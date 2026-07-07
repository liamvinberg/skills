"""Round-trip page listener. Stdlib only, long-lived, agent-agnostic.

Serve mode (default):
    python3 serve.py <dir> [--port N]
  Serves <dir> statically with no-store headers. POST /submit appends one
  JSON line to <dir>/answers.jsonl, stamps it server-side, and prints it
  to stdout as "SUBMIT <json>". Stays alive across any number of submits.

Await mode (for agents without a file-watch tool, or exit-to-wake loops):
    python3 serve.py --await <dir> [--after N] [--timeout SECS]
  Blocks until answers.jsonl holds more than N lines (default: its current
  count at start), prints the new lines, exits 0. Exits 2 on timeout.

The agent's loop: run serve once in the background, watch its output for
SUBMIT lines (or run --await), read the answer, rewrite state.json in
place. The page polls state.json and re-renders; the server never restarts.
"""
import argparse
import http.server
import json
import pathlib
import socketserver
import sys
import time


def count_lines(path: pathlib.Path) -> int:
    if not path.exists():
        return 0
    with path.open("rb") as f:
        return sum(1 for line in f if line.strip())


def await_mode(directory: pathlib.Path, after: int | None, timeout: float) -> int:
    log = directory / "answers.jsonl"
    baseline = count_lines(log) if after is None else after
    deadline = time.time() + timeout if timeout else None
    while True:
        n = count_lines(log)
        if n > baseline:
            lines = [l for l in log.read_text().splitlines() if l.strip()]
            for line in lines[baseline:]:
                print(line, flush=True)
            return 0
        if deadline and time.time() > deadline:
            print("timeout: no new answer", file=sys.stderr)
            return 2
        time.sleep(0.5)


def serve_mode(directory: pathlib.Path, port: int) -> int:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

        def do_POST(self):
            if self.path != "/submit":
                self.send_response(404)
                self.end_headers()
                return
            try:
                n = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(n) or b"{}")
            except (ValueError, json.JSONDecodeError):
                self.send_response(400)
                self.end_headers()
                return
            record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **payload} \
                if isinstance(payload, dict) else \
                {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "value": payload}
            line = json.dumps(record, ensure_ascii=False)
            with (directory / "answers.jsonl").open("a") as f:
                f.write(line + "\n")
            body = b'{"status":"ok"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            print(f"SUBMIT {line}", flush=True)

        def log_message(self, *args):
            pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), Handler) as srv:
        actual = srv.server_address[1]
        print(f"LISTENING http://127.0.0.1:{actual} dir={directory}", flush=True)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dir", type=pathlib.Path)
    p.add_argument("--port", type=int, default=0, help="0 picks a free port")
    p.add_argument("--await", dest="await_", action="store_true")
    p.add_argument("--after", type=int, default=None)
    p.add_argument("--timeout", type=float, default=0)
    a = p.parse_args()
    directory = a.dir.resolve()
    if not directory.is_dir():
        print(f"not a directory: {directory}", file=sys.stderr)
        return 1
    if a.await_:
        return await_mode(directory, a.after, a.timeout)
    return serve_mode(directory, a.port)


if __name__ == "__main__":
    sys.exit(main())
