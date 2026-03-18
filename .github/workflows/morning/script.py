import os
import requests

# If CLAUDE_REFRESH_TOKEN ever expires (401 error), re-extract it locally with:
#   security find-generic-password -s "Claude Code-credentials" -w | \
#     python3 -c "import sys,json; d=json.load(sys.stdin); print(d['claudeAiOauth']['refreshToken'])"
# Then update the CLAUDE_REFRESH_TOKEN secret in GitHub repo settings.

# Step 1: Refresh the OAuth access token
refresh_token = os.environ["CLAUDE_REFRESH_TOKEN"]

token_resp = requests.post(
    "https://platform.claude.com/v1/oauth/token",
    json={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": "9d1c250a-e61b-44d9-88ed-5944d1962f5e",
    },
)
token_resp.raise_for_status()
access_token = token_resp.json()["access_token"]

# Step 2: Send a message — authenticated via OAuth bearer token,
# which bills to the Claude.ai Pro plan (not the API).
msg_resp = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "Authorization": f"Bearer {access_token}",
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    },
    json={
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "ping"}],
    },
)
msg_resp.raise_for_status()
print("Morning session started — window resets at noon.")
