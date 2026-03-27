import csv
import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from msal import PublicClientApplication

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
if not CLIENT_ID:
    raise ValueError("Missing CLIENT_ID in .env file")

# For personal Outlook / Hotmail / Live accounts
AUTHORITY = "https://login.microsoftonline.com/consumers"

# Delegated scopes for signed-in user
SCOPES = ["User.Read", "Mail.Read", "Mail.Send"]

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
LOG_FILE = "matched_emails.csv"

# =========================
# CONFIG
# =========================
CHECK_TOP = 15
ONLY_UNREAD = True

KEYWORDS = [
    "internship",
    "interview",
    "cybersecurity",
    "application",
]

ALLOWED_SENDERS = [
    # "example@domain.com",
]

BLOCKED_SENDERS_CONTAINS = [
    "no-reply",
    "noreply",
    "donotreply",
]

ENABLE_AUTO_REPLY = False
AUTO_REPLY_TEXT = (
    "This is an automated reply.\n\n"
    "I received your email and will review it soon."
)
# =========================


def get_token() -> str:
    """
    Sign in using device code flow and return an access token.
    """
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )

    # Try cached token first
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]

    # Fall back to interactive device code flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError(f"Could not start device flow: {flow}")

    print("\nSign in to Microsoft:")
    print(flow["message"])
    print()

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise RuntimeError(f"Authentication failed:\n{result}")

    return result["access_token"]


def graph_get(endpoint: str, token: str, params=None) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    response = requests.get(
        f"{GRAPH_BASE}{endpoint}",
        headers=headers,
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def graph_post(endpoint: str, token: str, json_data: dict):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{GRAPH_BASE}{endpoint}",
        headers=headers,
        json=json_data,
        timeout=30,
    )
    response.raise_for_status()
    return response


def get_me(token: str) -> dict:
    return graph_get("/me", token)


def fetch_recent_messages(token: str, top: int = 10, only_unread: bool = False) -> list[dict]:
    params = {
        "$top": top,
        "$select": "id,subject,from,receivedDateTime,isRead,bodyPreview",
        "$orderby": "receivedDateTime DESC",
    }

    if only_unread:
        params["$filter"] = "isRead eq false"

    data = graph_get("/me/mailFolders/inbox/messages", token, params=params)
    return data.get("value", [])


def extract_sender_address(message: dict) -> str:
    return (
        message.get("from", {})
        .get("emailAddress", {})
        .get("address", "")
        .strip()
        .lower()
    )


def extract_subject(message: dict) -> str:
    return (message.get("subject") or "").strip()


def sender_is_blocked(sender: str) -> bool:
    sender_lower = sender.lower()
    return any(blocked in sender_lower for blocked in BLOCKED_SENDERS_CONTAINS)


def sender_is_allowed(sender: str) -> bool:
    if not ALLOWED_SENDERS:
        return True
    allowed_lower = [s.lower() for s in ALLOWED_SENDERS]
    return sender.lower() in allowed_lower


def message_matches(message: dict) -> bool:
    sender = extract_sender_address(message)
    subject = extract_subject(message).lower()
    preview = (message.get("bodyPreview") or "").lower()

    if not sender:
        return False

    if sender_is_blocked(sender):
        return False

    if not sender_is_allowed(sender):
        return False

    for keyword in KEYWORDS:
        keyword_lower = keyword.lower()
        if keyword_lower in subject or keyword_lower in preview:
            return True

    return False


def ensure_csv_exists(filepath: str):
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "logged_at_utc",
                "receivedDateTime",
                "sender",
                "subject",
                "isRead",
                "bodyPreview",
            ])


def log_message_to_csv(message: dict, filepath: str):
    ensure_csv_exists(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            message.get("receivedDateTime", ""),
            extract_sender_address(message),
            extract_subject(message),
            message.get("isRead", ""),
            (message.get("bodyPreview") or "").replace("\n", " ").strip(),
        ])


def send_email(token: str, to_email: str, subject: str, body_text: str):
    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body_text,
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to_email
                    }
                }
            ],
        },
        "saveToSentItems": True,
    }

    graph_post("/me/sendMail", token, payload)


def process_messages(token: str, messages: list[dict]) -> int:
    matched_count = 0

    me = get_me(token)
    my_email = (me.get("mail") or me.get("userPrincipalName") or "").lower()

    for msg in messages:
        sender = extract_sender_address(msg)
        subject = extract_subject(msg)
        is_read = msg.get("isRead", False)

        print(f"Checking: {sender or 'unknown sender'} | {subject or 'No Subject'} | isRead={is_read}")

        if not message_matches(msg):
            continue

        matched_count += 1
        print("  -> MATCHED")
        log_message_to_csv(msg, LOG_FILE)

        if ENABLE_AUTO_REPLY and sender and sender != my_email:
            reply_subject = f"Re: {subject}" if subject else "Re:"
            send_email(token, sender, reply_subject, AUTO_REPLY_TEXT)
            print(f"  -> Auto-replied to {sender}")

    return matched_count


def main():
    print("Starting Outlook bot...")

    token = get_token()

    me = get_me(token)
    signed_in_as = me.get("mail") or me.get("userPrincipalName") or "Unknown"
    print(f"Signed in as: {signed_in_as}\n")

    messages = fetch_recent_messages(
        token=token,
        top=CHECK_TOP,
        only_unread=ONLY_UNREAD,
    )

    print(f"Fetched {len(messages)} message(s)\n")

    matched_count = process_messages(token, messages)

    print("\nDone.")
    print(f"Matched emails: {matched_count}")
    print(f"Log file: {LOG_FILE}")


if __name__ == "__main__":
    main()