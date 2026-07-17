---
name: beam
description: Explicit invocation only. Use only after the user types `beam`, `$beam`, or `/beam` as the requested skill in the current request. Never activate from task content alone. Once invoked, temporarily serve a local file or folder to the user's other devices over their Tailscale tailnet.
argument-hint: "[path]"
disable-model-invocation: true
---

# Beam

Serve a local path over the user's private network so any of their devices can open it in a browser. One pattern everywhere: a localhost static server, proxied by Tailscale serve. HTTPS, stable hostname, tailnet-only.

## Steps

1. Resolve the target to an absolute path. A page with assets beams as its whole directory; a single file beams as its parent directory, linked by filename. Done when the path exists on disk.
2. Start the local server: `nohup python3 -m http.server 8330 --bind 127.0.0.1 --directory "<dir>" >/dev/null 2>&1 &` and note the pid (next free port if 8330 is taken). The 127.0.0.1 bind keeps the tailnet proxy the only door in. Done when `curl http://127.0.0.1:8330/` returns 200.
3. Proxy it: `tailscale serve --bg 8330`. CLI lives on PATH or at `/Applications/Tailscale.app/Contents/MacOS/Tailscale`. Done when the command prints the https tailnet URL. (Serving a filesystem path directly, without the local server, fails on the macOS GUI app: sandbox restriction. The proxy pattern is why this skill has one path.)
4. Verify before reporting: curl the tailnet URL with retries until it returns 200 and the expected content. The first https hit can lag a few seconds while the cert provisions.
5. Report the URL (append the filename for a single file), the server pid, and the stop recipe below.

## Stopping a beam

- `tailscale serve --https=443 off` stops the proxy (`tailscale serve reset` clears every serve rule); `kill <pid>` stops the local server.
- `tailscale serve status` shows what is currently live.

## Guardrails

- serve is tailnet-only: reachable by the user's own devices, nothing else. `tailscale funnel` publishes to the open internet; reach for it only when the user explicitly asks for a public link.
- No Tailscale on the machine: run the same local server bound to `0.0.0.0` and report `http://<LAN IP>:<port>/`, noting it is reachable by anyone on the same network.
- Browsers render html and images natively; markdown arrives as plain text. When the user wants markdown readable, offer to convert it to html first, then beam that.
