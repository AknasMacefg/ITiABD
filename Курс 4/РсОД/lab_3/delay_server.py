"""Serve a generated catalog with an optional delay per request."""

from __future__ import annotations

import argparse
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class DelayedHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, delay: float = 0.0, **kwargs):
        self.delay = delay
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        if self.delay > 0:
            time.sleep(self.delay)
        super().do_GET()

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--delay", type=float, default=0.12)
    args = parser.parse_args()
    handler = partial(DelayedHandler, directory=str(args.dir), delay=args.delay)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Serving {args.dir} at http://127.0.0.1:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
