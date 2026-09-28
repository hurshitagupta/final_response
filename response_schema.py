from dataclasses import dataclass, asdict
from typing import Literal
import json
import time

Status = Literal["success", "failure", "partial"]

@dataclass
class FinalResponse:
    answer: str
    status: Status
    completed_action: str
    warnings: list[str]
    next_action: str | None


def build_response(result: str, status: Status, completed_action: str, warning: str = "", next_action: str | None = None) -> FinalResponse:

    if not result.strip():
        raise ValueError("Result cannot be empty.")

    if status not in {"success", "failure", "partial"}:
        raise ValueError("Invalid response status.")

    warnings = [warning] if warning else []

    if status == "success":
        answer = result
    elif status == "partial":
        answer = f"Partially completed: {result}"
    else:
        answer = f"Unable to complete: {result}"

    return FinalResponse(answer=answer, status=status, completed_action=completed_action, warnings=warnings, next_action=next_action)


def main():
    start_time = time.perf_counter()

    print("=== RESPONSE SCHEMA ===\n")

    print("Happy Path:")
    success_response = build_response(result="Report generated successfully.", status="success", completed_action="Generated the requested report.")

    print(json.dumps(asdict(success_response), indent=2))

    print("\nFailure Path:")
    failure_response = build_response(result="Required data was unavailable.", status="failure", completed_action="Checked available report data.", warning="Some required data could not be found.", next_action="Provide the missing report data and try again.")

    print(json.dumps(asdict(failure_response), indent=2))

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print("\n=== MEASUREMENT ===")
    print("Responses created: 2")
    print(f"Processing time: {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    main()