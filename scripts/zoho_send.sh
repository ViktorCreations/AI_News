#!/usr/bin/env bash
# Send a newsletter issue by email via the Zoho Mail REST API (HTTPS — works
# through the environment's egress proxy; raw SMTP ports are blocked).
#
# Usage: scripts/zoho_send.sh newsletters/YYYY-MM-DD.md
#
# Credentials live OUTSIDE the repo in ~/.zoho_mail_api (never commit them):
#   CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN  — Zoho self-client OAuth
#   ACCOUNT_ID / FROM_ADDRESS / TO_ADDRESS     — send parameters
# First-time setup: see the comments inside ~/.zoho_mail_api. If REFRESH_TOKEN
# is empty but GRANT_CODE is set, this script performs the one-time exchange
# and persists the refresh token.
set -euo pipefail

ISSUE="${1:?usage: zoho_send.sh newsletters/YYYY-MM-DD.md}"
CRED_FILE="${ZOHO_CRED_FILE:-$HOME/.zoho_mail_api}"
CA="--cacert /root/.ccr/ca-bundle.crt"
[ -f "$CRED_FILE" ] || { echo "ERROR: $CRED_FILE not found"; exit 1; }
# shellcheck source=/dev/null
source "$CRED_FILE"

# One-time: exchange a fresh grant code for a permanent refresh token.
if [ -z "${REFRESH_TOKEN:-}" ]; then
  [ -n "${GRANT_CODE:-}" ] && [ "$GRANT_CODE" != "PASTE_GRANT_CODE_HERE" ] \
    || { echo "ERROR: no REFRESH_TOKEN and no GRANT_CODE in $CRED_FILE"; exit 1; }
  RESP=$(curl -sS $CA -X POST "https://accounts.zoho.com/oauth/v2/token" \
    -d "grant_type=authorization_code" -d "code=$GRANT_CODE" \
    -d "client_id=$CLIENT_ID" -d "client_secret=$CLIENT_SECRET")
  REFRESH_TOKEN=$(printf '%s' "$RESP" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("refresh_token",""))')
  [ -n "$REFRESH_TOKEN" ] || { echo "ERROR: grant-code exchange failed: $RESP"; exit 1; }
  sed -i "s|^REFRESH_TOKEN=.*|REFRESH_TOKEN=$REFRESH_TOKEN|; s|^GRANT_CODE=.*|GRANT_CODE=used|" "$CRED_FILE"
  echo "Refresh token obtained and saved."
fi

ACCESS_TOKEN=$(curl -sS $CA -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=refresh_token" -d "refresh_token=$REFRESH_TOKEN" \
  -d "client_id=$CLIENT_ID" -d "client_secret=$CLIENT_SECRET" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin).get("access_token",""))')
[ -n "$ACCESS_TOKEN" ] || { echo "ERROR: access-token refresh failed"; exit 1; }

SUBJECT=$(head -1 "$ISSUE" | sed 's/^# //')
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PAYLOAD=$(python3 - "$ISSUE" "$FROM_ADDRESS" "$TO_ADDRESS" "$SUBJECT" <<'PYEOF'
import sys, json, importlib.util, os
issue, from_addr, to_addr, subject = sys.argv[1:5]
# locate md2email.py relative to the issue file's repo root
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(issue)))
spec = importlib.util.spec_from_file_location("md2email", os.path.join(repo_root, "scripts", "md2email.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
html = mod.convert(open(issue).read())
print(json.dumps({"fromAddress": from_addr, "toAddress": to_addr,
                  "subject": subject, "content": html, "mailFormat": "html"}))
PYEOF
)

HTTP=$(curl -sS $CA -o /tmp/zoho_send_resp.json -w "%{http_code}" \
  -X POST "https://mail.zoho.com/api/accounts/$ACCOUNT_ID/messages" \
  -H "Authorization: Zoho-oauthtoken $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary "$PAYLOAD")
if [ "$HTTP" = "200" ]; then
  echo "Email sent: \"$SUBJECT\" -> $TO_ADDRESS"
else
  echo "ERROR: send failed (HTTP $HTTP): $(cat /tmp/zoho_send_resp.json)"; exit 1
fi
