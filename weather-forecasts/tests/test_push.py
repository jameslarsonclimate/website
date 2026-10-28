"""Deadline reminders (wxc_push.py): message bag, time window, once a day, pause, dropped
phones, and a real encrypted push to a fake push service (decrypted and its VAPID JWT checked)."""
import base64
import json
import os
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

import wxc_push as wp


@pytest.fixture(autouse=True)
def conf(tmp_path, monkeypatch):
    monkeypatch.setattr(wp, "CONF", tmp_path)
    for name, f in [("KEY", "vapid_private.pem"), ("SUBS", "subscriptions.json"), ("STATE", "state.json"),
                    ("PAUSED", "paused")]:
        monkeypatch.setattr(wp, name, tmp_path / f)
    wp.make_keys()
    return tmp_path


def b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def sub(endpoint="https://web.push.apple.com/abc"):
    return {"endpoint": endpoint, "keys": {"p256dh": "BOrx", "auth": "a1"}}


def at(h, m):
    return datetime(2026, 10, 28, h, m, tzinfo=timezone.utc)


def test_messages_and_bag():
    assert len(wp.MESSAGES) == 36 and len(set(wp.MESSAGES)) == 36
    state, seen = {}, []
    for _ in range(36):
        seen.append(wp.next_message(state))
    assert sorted(seen) == sorted(wp.MESSAGES)                    # every one once per round
    last = seen[-1]
    assert wp.next_message(state) != last                         # no repeat across a refill


def test_window_and_add():
    assert not wp.in_window(at(21, 49)) and wp.in_window(at(21, 50)) and wp.in_window(at(22, 0))
    assert wp.in_window(at(23, 29)) and not wp.in_window(at(23, 30)) and not wp.in_window(at(0, 5))
    assert not wp.add_subscription("hello") and not wp.add_subscription('{"endpoint": "x"}')
    assert wp.add_subscription(json.dumps(sub())) and wp.add_subscription(json.dumps(sub()))
    assert len(json.loads(wp.SUBS.read_text())) == 1                # same phone: replaced


def test_send_once_a_day_and_pause():
    calls = []
    fake = lambda **kw: calls.append(kw)
    assert "no phones" in wp.send(now=at(22, 0), webpush=fake)
    wp.add_subscription(json.dumps(sub()))
    assert "outside" in wp.send(now=at(21, 0), webpush=fake) and not calls
    assert "'sent': 1" in wp.send(now=at(22, 0), webpush=fake)
    assert "already sent" in wp.send(now=at(23, 0), webpush=fake) and len(calls) == 1
    assert "test" in wp.send(test=True, now=at(23, 0), webpush=fake) and len(calls) == 2
    p = json.loads(calls[0]["data"])
    assert p["title"] == wp.TITLE and p["body"] in wp.MESSAGES and p["url"] == wp.PAGE
    assert calls[0]["vapid_claims"] == {"sub": wp.CONTACT} and calls[0]["ttl"] == 7200
    wp.PAUSED.touch()
    assert "paused" in wp.send(now=at(22, 0).replace(day=29), webpush=fake) and len(calls) == 2


def test_gone_phone_is_dropped():
    class Gone(Exception):
        def __init__(self, code):
            self.response = type("R", (), {"status_code": code})()
    wp.add_subscription(json.dumps(sub("https://a.example/1")))
    wp.add_subscription(json.dumps(sub("https://b.example/2")))
    wp.add_subscription(json.dumps(sub("https://c.example/3")))

    def fake(subscription_info, **kw):
        if "a.example" in subscription_info["endpoint"]:
            raise Gone(410)
        if "b.example" in subscription_info["endpoint"]:
            raise Gone(500)
    assert wp.push_all("hi", webpush=fake) == {"sent": 1, "dropped": 1, "failed": 1}
    assert [s["endpoint"] for s in json.loads(wp.SUBS.read_text())] == ["https://b.example/2", "https://c.example/3"]


def test_real_push_decrypts():
    """The full pywebpush path against a local endpoint: aes128gcm payload and a valid VAPID JWT."""
    import http_ece
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature

    phone = ec.generate_private_key(ec.SECP256R1())
    auth = os.urandom(16)
    pub = phone.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    got = {}

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            got["headers"] = dict(self.headers)
            got["body"] = self.rfile.read(int(self.headers["Content-Length"]))
            self.send_response(201)
            self.end_headers()

        def log_message(self, *a):
            pass
    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.handle_request, daemon=True).start()
    endpoint = f"http://127.0.0.1:{srv.server_port}/push/xyz"
    wp.add_subscription(json.dumps({"endpoint": "https://x", "keys": {"p256dh": b64(pub), "auth": b64(auth)}}))
    subs = json.loads(wp.SUBS.read_text())
    subs[0]["endpoint"] = endpoint                   # add() only takes https endpoints
    wp.SUBS.write_text(json.dumps(subs))
    assert wp.push_all("Two hours left.") == {"sent": 1, "dropped": 0, "failed": 0}
    srv.server_close()

    h = {k.lower(): v for k, v in got["headers"].items()}
    assert h["content-encoding"] == "aes128gcm" and h["ttl"] == "7200" and h["urgency"] == "high"
    plain = json.loads(http_ece.decrypt(got["body"], private_key=phone, auth_secret=auth, version="aes128gcm"))
    assert plain == {"title": wp.TITLE, "body": "Two hours left.", "url": wp.PAGE, "tag": "wxc-deadline"}

    # VAPID: "vapid t=<jwt>, k=<our public key>", signed by our key, for this push service's origin
    auth_h = h["authorization"]
    jwt = auth_h.split("t=")[1].split(",")[0].strip()
    assert auth_h.split("k=")[1].strip() == wp.public_key()
    head, claims, sig = jwt.split(".")
    pad = lambda s: base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
    c = json.loads(pad(claims))
    assert c["aud"] == f"http://127.0.0.1:{srv.server_port}" and c["sub"] == wp.CONTACT
    raw = pad(sig)
    der = encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"))
    vapid_pub = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), pad(wp.public_key()))
    vapid_pub.verify(der, f"{head}.{claims}".encode(), ec.ECDSA(hashes.SHA256()))   # raises if bad
