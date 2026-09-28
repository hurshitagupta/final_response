import re
import time


EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE_PATTERN = r"\b\d{10}\b"
API_KEY_PATTERN = r"\bsk-[A-Za-z0-9_-]+\b"


def redact_sensitive_data(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    if not text.strip():
        raise ValueError("Input text cannot be empty.")

    redacted = text

    redacted = re.sub(EMAIL_PATTERN, "[REDACTED_EMAIL]", redacted)

    redacted = re.sub(PHONE_PATTERN, "[REDACTED_PHONE]", redacted)

    redacted = re.sub(API_KEY_PATTERN, "[REDACTED_API_KEY]", redacted)

    return redacted


def main():
    start_time = time.perf_counter()

    print("=== REDACTION ===\n")

    print("Happy Path:")

    safe_text = "Report generated successfully for the customer."

    safe_result = redact_sensitive_data(safe_text)

    print("Original:", safe_text)
    print("Final:", safe_result)

    print("\nSensitive Data Path:")

    sensitive_text = (
        "Send the report to user@example.com. "
        "Contact number is 9876543210. "
        "API key is sk-demo12345."
    )

    redacted_result = redact_sensitive_data(sensitive_text)

    print("Original:", sensitive_text)
    print("Redacted:", redacted_result)

    redaction_count = redacted_result.count("[REDACTED_")

    print("\nFailure / Rejection Path:")

    try:
        redact_sensitive_data("")
    except ValueError as error:
        print("Rejected input:", error)

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print("\n=== MEASUREMENT ===")
    print(f"Sensitive values redacted: {redaction_count}")
    print("Rejected inputs: 1")
    print(f"Processing time: {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    main()