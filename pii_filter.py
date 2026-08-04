import re

# ==========================================================
# Regex Patterns
# ==========================================================

EMAIL_PATTERN = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b"

PHONE_PATTERN = r"\b(?:\+?\d{1,3}[- ]?)?(?:\d{10})\b"

PASSPORT_PATTERN = r"\b[A-Z][0-9]{7}\b"

CARD_PATTERN = r"\b(?:\d[ -]*?){13,16}\b"


# ==========================================================
# PII Masking
# ==========================================================

def mask_pii(text: str) -> str:
    """
    Masks commonly occurring Personally Identifiable Information (PII)
    before sending the response to the user.
    """

    if not text:
        return text

    # Email
    text = re.sub(
        EMAIL_PATTERN,
        "[EMAIL REDACTED]",
        text,
    )

    # Phone Number
    text = re.sub(
        PHONE_PATTERN,
        "[PHONE REDACTED]",
        text,
    )

    # Passport Number
    text = re.sub(
        PASSPORT_PATTERN,
        "[PASSPORT REDACTED]",
        text,
    )

    # Credit / Debit Card Number
    text = re.sub(
        CARD_PATTERN,
        "[CARD REDACTED]",
        text,
    )

    return text