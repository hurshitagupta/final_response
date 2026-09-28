import pytest

from redaction import redact_sensitive_data


def test_safe_text_remains_unchanged():
    text = "Report generated successfully."

    result = redact_sensitive_data(text)

    assert result == text


def test_email_is_redacted():
    text = "Send the report to user@example.com."

    result = redact_sensitive_data(text)

    assert "user@example.com" not in result
    assert "[REDACTED_EMAIL]" in result


def test_phone_number_is_redacted():
    text = "Contact the user on 9876543210."

    result = redact_sensitive_data(text)

    assert "9876543210" not in result
    assert "[REDACTED_PHONE]" in result


def test_api_key_is_redacted():
    text = "API key is sk-demo12345."

    result = redact_sensitive_data(text)

    assert "sk-demo12345" not in result
    assert "[REDACTED_API_KEY]" in result


def test_empty_input_is_rejected():
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        redact_sensitive_data("")


def test_non_string_input_is_rejected():
    with pytest.raises(ValueError, match="Input must be a string"):
        redact_sensitive_data(12345)