import argparse
import base64
import hashlib
import hmac
import json
from pathlib import Path


def verify_manifest(manifest_path: Path, secret: str) -> bool:
    payload = json.loads(manifest_path.read_text(encoding='utf-8'))
    signature = base64.b64decode(payload['signature'])
    unsigned = json.dumps(payload['manifest'], sort_keys=True, separators=(',', ':')).encode('utf-8')
    expected = hmac.new(secret.encode('utf-8'), unsigned, hashlib.sha256).digest()
    return hmac.compare_digest(signature, expected)


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify signed update manifest')
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--secret', required=True)
    args = parser.parse_args()

    if verify_manifest(args.manifest, args.secret):
        print('VALID')
        return 0

    print('INVALID')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())