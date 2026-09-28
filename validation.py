from dataclasses import dataclass
import time


@dataclass
class ResponseData:
    answer: str
    status: str
    completed_action: str
    warnings: list[str]
    next_action: str | None


def validate_response(response: ResponseData) -> bool:
    allowed_statuses = {"success", "failure", "partial"}

    if not response.answer.strip():
        raise ValueError("Answer cannot be empty.")

    if response.status not in allowed_statuses:
        raise ValueError("Invalid response status.")

    if not response.completed_action.strip():
        raise ValueError("Completed action cannot be empty.")

    if response.status == "failure" and not response.next_action:
        raise ValueError("Failure response must include a next action.")

    if response.status == "partial" and not response.warnings:
        raise ValueError("Partial response must include at least one warning.")

    return True


def main():
    start_time = time.perf_counter()

    print("=== VALIDATION ===\n")

    print("Happy Path:")

    success_response = ResponseData(answer="Report generated successfully.", status="success", completed_action="Generated the requested report.", warnings=[], next_action=None)

    result = validate_response(success_response)

    print("Valid response:", result)
    print("Status:", success_response.status)
    print("Answer:", success_response.answer)

    print("\nFailure / Rejection Path:")

    invalid_response = ResponseData(answer="Unable to complete the report.", status="failure", completed_action="Checked the available report data.", warnings=["Required report data is missing."], next_action=None)

    try:
        validate_response(invalid_response)

    except ValueError as error:
        print("Rejected response:", error)

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print("\n=== MEASUREMENT ===")
    print("Responses checked: 2")
    print("Valid responses: 1")
    print("Rejected responses: 1")
    print(f"Processing time: {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    main()