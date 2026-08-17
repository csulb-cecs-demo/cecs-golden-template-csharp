#!/usr/bin/env python3
"""Minimal reference service for the performance sanity check.

Exists so `perf/smoke.js` runs out of the box, with nothing to install and
nothing to configure. It is a stand-in, not the thing being assessed.

================================================================================
FACULTY: replace this with your own service
================================================================================

For an assignment that builds a web app or API, delete this file and point the
workflow at the student's service instead — set BASE_URL and start their app in
place of this one. The k6 script needs no changes.

Kept deliberately dependency-free (standard library only, no Flask, no
FastAPI). A perf harness that fails because a package index was slow is worse
than no perf harness: it produces red builds that teach students to ignore red
builds.

ThreadingHTTPServer, not HTTPServer: the default is single-threaded and would
serialize 75 concurrent virtual users into a queue. The measurement would then
be of this stand-in's inadequacy rather than of anything meaningful.

Usage:
    python3 perf/reference_service.py            # port 8080
    PORT=9000 python3 perf/reference_service.py
"""

import json
import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # keep-alive; matches how a real client behaves

    def do_GET(self):
        if self.path in ("/", "/health"):
            self._respond(200, {"status": "ok", "service": "reference"})
        else:
            self._respond(404, {"error": "not found", "path": self.path})

    def _respond(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        # Silence per-request logging. 75 VUs for 45 seconds is thousands of
        # lines that bury the k6 report in the build log.
        pass


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    server.daemon_threads = True

    def shutdown(signum, frame):
        server.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    print(f"reference service listening on http://127.0.0.1:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
