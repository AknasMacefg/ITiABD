import base64
import hashlib
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


def is_manifest_valid(manifest_path: Path, secret: str) -> bool:
    if not manifest_path.exists():
        return False

    payload = json.loads(manifest_path.read_text(encoding='utf-8'))
    signature = base64.b64decode(payload['signature'])
    unsigned = json.dumps(payload['manifest'], sort_keys=True, separators=(',', ':')).encode('utf-8')
    expected = hmac.new(secret.encode('utf-8'), unsigned, hashlib.sha256).digest()
    return hmac.compare_digest(signature, expected)


class GuardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/health'):
            self.send_response(404)
            self.end_headers()
            return

        manifest_path = Path(os.environ.get('MANIFEST_PATH', '/app/security/update_manifest.json'))
        secret = os.environ.get('UPDATE_GUARD_SECRET', 'dev-secret')
        valid = is_manifest_valid(manifest_path, secret)
        body = json.dumps({'status': 'ok' if valid else 'blocked', 'manifest_valid': valid}).encode('utf-8')

        self.send_response(200 if valid else 403)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    port = int(os.environ.get('PORT', '9000'))
    server = HTTPServer(('0.0.0.0', port), GuardHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()