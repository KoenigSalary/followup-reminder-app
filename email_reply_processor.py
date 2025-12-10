# email_reply_processor.py

"""
Provides process_inbox_replies() used by streamlit_app.py.

Currently implemented as a safe stub:
- Returns an empty list (no replies)
- Prevents import errors
- Can be extended later to actually read and process email replies.
"""

from typing import List, Dict, Any

def process_inbox_replies() -> List[Dict[str, Any]]:
    """
    Stub implementation.

    In the future, this can:
    - Connect to your email inbox (IMAP/API)
    - Read follow-up replies
    - Map them to tasks / MoM entries

    For now, it just returns an empty list so that
    the rest of the app can run without crashing.
    """
    return []
