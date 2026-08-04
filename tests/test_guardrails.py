from pii_filter import mask_pii


def test_email():

    result = mask_pii(
        "Contact me at john@gmail.com"
    )

    assert "[EMAIL REDACTED]" in result


def test_phone():

    result = mask_pii(
        "9876543210"
    )

    assert "[PHONE REDACTED]" in result


def test_passport():

    result = mask_pii(
        "Passport A1234567"
    )

    assert "[PASSPORT REDACTED]" in result


def test_card():

    result = mask_pii(
        "1234 5678 9012 3456"
    )

    assert "[CARD REDACTED]" in result