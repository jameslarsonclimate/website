"""
Deadline reminders for the WxChallenge home-screen app (Web Push; iPhone 16.4+ home-screen
app, Android Chrome / Firefox): one notification two hours before the 00Z deadline, at 22Z on
the evenings before forecast days (Sun-Wed evenings for the Mon-Thu forecast days).

  python wxc_push.py keys          make the VAPID key pair (once) and print the public key,
                                   which goes in wxchallenge/app.js (VAPID_PUBLIC)
  python wxc_push.py add [FILE]    add a phone: the code the page shows after "Remind me"
                                   (from FILE, stdin, or the clipboard via pbpaste)
  python wxc_push.py list          the phones it sends to
  python wxc_push.py send          send the reminder, only from 21:50Z to 23:30Z and once per
                                   UTC day (launchd starts it, see install_wxc_reminder.sh)
  python wxc_push.py send --test   send one now, whatever the time (not counted for the day)
  python wxc_push.py pause|resume  stop / restart the reminders (contest breaks)

Private files (never in the repo) live in ~/.config/wxc-push/: the VAPID private key, the
subscriptions and the state (the day last sent, the shuffled message bag). Phones that have
gone away (404/410 from the push service) are dropped. The VAPID "sub" claim is the site's
origin, not an email address.
"""
import argparse
import json
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CONF = Path.home() / ".config" / "wxc-push"
KEY = CONF / "vapid_private.pem"
SUBS = CONF / "subscriptions.json"
STATE = CONF / "state.json"
PAUSED = CONF / "paused"
PAGE = "https://jameslarsonclimate.github.io/website/weather-forecasts/wxchallenge/"
CONTACT = "https://jameslarsonclimate.github.io"   # VAPID "sub": an https origin (no path) or mailto:
TITLE = "WxChallenge: forecast due at 00Z"
WINDOW = ((21, 50), (23, 30))     # UTC: send only inside this (the deadline is 00Z)

# approved by James 2026-10-28 (1-14, 17-35 and 48-50 of the 50 drafts)
MESSAGES = [
    "The clouds held a meeting. They want your forecast in 2 hours.",
    "Your forecast is due in 2 hours. The HRRR has already changed its mind 4 times.",
    "🐸 A frog told me it's going to rain. Submit before he does.",
    "Two hours left. Even the GFS has submitted, and it doesn't know what day it is.",
    "Breaking: local meteorologist still hasn't submitted. More at 7.",
    "Your high temp is lonely. Give it a low to hang out with. 2 hours.",
    "The ensembles took a vote: 51 to 0 that you should submit now.",
    "Beep boop. This is NBM. I am calibrated. Are you? Deadline in 2 h.",
    "Roses are red, METARs are blue, your forecast's not in, and 00Z's coming for you.",
    "Somewhere a weather balloon just popped thinking about your empty forecast.",
    "Two hours left to submit. Don't be shy, everyone does it eventually.",
    "It's not the size of your precip, it's how accurate it is. 2 hours.",
    "Your forecast is looking a little unstable tonight… 😏 2 hours to deadline.",
    "CAPE is high, and so is the tension. Submit.",
    "Nothing's more attractive than a well-calibrated low. Submit it.",
    "Slide into the WxChallenge form. You've got 2 hours.",
    "You know you want to put a number in that box. 😉",
    "Lower your inhibitions, not your low temperature. 2 hours left.",
    "Oh no, take your time. It's not like there's a deadline in 2 hours or anything.",
    "Bold strategy: not submitting. Let's see if it pays off.",
    "Sure, check the HRRR one more time. That'll fix it.",
    "Persistence forecasting, also known as \"I forgot.\" 2 hours.",
    "Congrats, you've stared at Pivotal Weather for 3 hours. Now type four numbers.",
    "The consensus is right there and you still haven't copied it. Impressive restraint.",
    "Your error points called. They're bored without you.",
    "\"I'll do it later,\" you said, 6 hours ago. It's later.",
    "Reminder: climatology beats people who don't submit.",
    "A forecast you never submit is 100% wrong. Great job so far.",
    "No pressure, but everyone else submitted at noon.",
    "It would be a shame if something happened to your ranking. 2 hours.",
    "Just checking in! 😊 Deadline in 2 hours! Totally fine! 😊",
    "Per my last notification, please submit your forecast.",
    "Your advisor can see the standings, you know.",
    "🚨 Weather emergency: forecast not submitted. 2 hours to 00Z.",
    "Brought to you by your future self, who's tired of seeing you at the bottom of the standings.",
    "Last call at the WxChallenge bar. Two hours, then the taps close.",
]


def _load(path: Path, default):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, ValueError):
        return default


def _save(path: Path, obj):
    CONF.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, indent=1, ensure_ascii=False))
    tmp.replace(path)
    path.chmod(0o600)


def in_window(now: datetime) -> bool:
    (h0, m0), (h1, m1) = WINDOW
    return (h0, m0) <= (now.hour, now.minute) < (h1, m1)


def next_message(state: dict, rng=random) -> str:
    """Draw from a shuffled bag of message indices, so none repeats until all have been used."""
    bag = [i for i in state.get("bag", []) if 0 <= i < len(MESSAGES)]
    if not bag:
        bag = list(range(len(MESSAGES)))
        rng.shuffle(bag)
        if state.get("last") in bag[:1] and len(bag) > 1:     # no repeat across a refill
            bag.append(bag.pop(0))
    i = bag.pop(0)
    state["bag"], state["last"] = bag, i
    return MESSAGES[i]


def public_key() -> str:
    from py_vapid import Vapid, b64urlencode
    from cryptography.hazmat.primitives import serialization
    v = Vapid.from_file(str(KEY))
    raw = v.public_key.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    return b64urlencode(raw)


def make_keys():
    from py_vapid import Vapid
    if not KEY.exists():
        CONF.mkdir(parents=True, exist_ok=True)
        v = Vapid()
        v.generate_keys()
        v.save_key(str(KEY))
        KEY.chmod(0o600)
        print(f"New VAPID key: {KEY}")
    print("Public key (VAPID_PUBLIC in wxchallenge/app.js):")
    print(public_key())


def add_subscription(text: str) -> bool:
    """Add the subscription JSON the page shows; False if it isn't one. Same endpoint: replaced."""
    try:
        sub = json.loads(text.strip())
        assert sub["endpoint"].startswith("https://") and sub["keys"]["p256dh"] and sub["keys"]["auth"]
    except (ValueError, KeyError, TypeError, AssertionError, AttributeError):
        return False
    subs = [s for s in _load(SUBS, []) if s["endpoint"] != sub["endpoint"]]
    subs.append({"endpoint": sub["endpoint"], "keys": sub["keys"],
                 "added_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")})
    _save(SUBS, subs)
    return True


def push_all(body: str, webpush=None) -> dict:
    """Send one notification to every subscription; drop the ones the push service says are gone."""
    if webpush is None:
        from pywebpush import webpush
    from urllib.parse import urlparse
    payload = json.dumps({"title": TITLE, "body": body, "url": PAGE, "tag": "wxc-deadline"})
    subs, keep, out = _load(SUBS, []), [], {"sent": 0, "dropped": 0, "failed": 0}
    for s in subs:
        host = urlparse(s["endpoint"]).netloc
        try:
            webpush(subscription_info={"endpoint": s["endpoint"], "keys": s["keys"]}, data=payload,
                    vapid_private_key=str(KEY), vapid_claims={"sub": CONTACT}, ttl=2 * 3600,
                    headers={"Urgency": "high"})
            out["sent"] += 1
            keep.append(s)
        except Exception as exc:          # pywebpush.WebPushException carries the response
            code = getattr(getattr(exc, "response", None), "status_code", None)
            if code in (404, 410):
                out["dropped"] += 1
                print(f"  {host}: gone ({code}), removed")
                continue
            out["failed"] += 1
            keep.append(s)
            print(f"  {host}: failed ({code or type(exc).__name__}: {str(exc)[:160]})")
    if out["dropped"]:
        _save(SUBS, keep)
    return out


def send(test=False, now=None, webpush=None) -> str:
    now = now or datetime.now(timezone.utc)
    day = now.strftime("%Y-%m-%d")
    state = _load(STATE, {})
    if not test:
        if PAUSED.exists():
            return "paused (python wxc_push.py resume to restart)"
        if not in_window(now):
            return f"outside the {WINDOW[0][0]}:{WINDOW[0][1]:02d}-{WINDOW[1][0]}:{WINDOW[1][1]:02d}Z window, not sent"
        if state.get("sent_day") == day:
            return f"already sent for {day}"
    if not _load(SUBS, []):
        return "no phones added yet (python wxc_push.py add)"
    body = next_message(state)
    res = push_all(body, webpush)
    if res["sent"] and not test:
        state["sent_day"] = day
    _save(STATE, state)
    return f"{'test ' if test else ''}reminder: {res} | {body}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("cmd", choices=["keys", "add", "list", "send", "pause", "resume"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--test", action="store_true", help="send now, whatever the time")
    a = ap.parse_args(argv)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if a.cmd == "keys":
        make_keys()
    elif a.cmd == "add":
        text = (Path(a.file).read_text() if a.file else
                sys.stdin.read() if not sys.stdin.isatty() else
                subprocess.run(["pbpaste"], capture_output=True, text=True).stdout)
        if not add_subscription(text):
            sys.exit("That isn't a subscription code (copy it from the page after tapping \"Remind me\").")
        print(f"Added. {len(_load(SUBS, []))} phone(s) now.")
    elif a.cmd == "list":
        for s in _load(SUBS, []):
            print(f"{s.get('added_utc', '?')}  {s['endpoint'][:70]}…")
    elif a.cmd == "pause":
        CONF.mkdir(parents=True, exist_ok=True)
        PAUSED.touch()
        print("Reminders paused.")
    elif a.cmd == "resume":
        PAUSED.unlink(missing_ok=True)
        print("Reminders on.")
    else:
        print(f"{stamp}: {send(test=a.test)}")


if __name__ == "__main__":
    main()
