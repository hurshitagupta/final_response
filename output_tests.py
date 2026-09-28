from dataclasses import dataclass
import time


@dataclass
class FinalOutput:
    answer: str
    status: str
    completed_action: str
    warnings: list[str]
    next_action: str | None


def check_final_output(output: FinalOutput) -> bool:
    allowed_statuses = {"success", "failure", "partial"}

    if not output.answer.strip():
        raise ValueError("Final answer cannot be empty.")

    if output.status not in allowed_statuses:
        raise ValueError("Invalid final output status.")

    if not output.completed_action.strip():
        raise ValueError("Completed action is required.")

    if output.status == "failure" and not output.next_action:
        raise ValueError("Failure output must include a next action.")

    if output.status == "partial" and not output.warnings:
        raise ValueError("Partial output must include a warning.")

    blocked_markers = ["INTERNAL NOTE:", "DEBUG:", "SYSTEM:", "TOOL_CALL:"]

    for marker in blocked_markers:
        if marker.lower() in output.answer.lower():
            raise ValueError(f"Final output contains blocked internal content: {marker}")

    return True


def main():
    start_time = time.perf_counter()

    print("=== OUTPUT TESTS ===\n")

    print("Happy Path:")

    valid_output = FinalOutput(answer="The requested report has been generated successfully.", status="success", completed_action="Generated the requested report.", warnings=[], next_action=None)

    result = check_final_output(valid_output)

    print("Output valid:", result)
    print("Status:", valid_output.status)
    print("Answer:", valid_output.answer)

    print("\nFailure / Rejection Path:")

    invalid_output = FinalOutput(answer=("Report generated. INTERNAL NOTE: verify record 25 manually."),status="success", completed_action="Generated the requested report.", warnings=[], next_action=None)

    try:
        check_final_output(invalid_output)

    except ValueError as error:
        print("Rejected output:", error)

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print("\n=== MEASUREMENT ===")
    print("Outputs checked: 2")
    print("Valid outputs: 1")
    print("Rejected outputs: 1")
    print(f"Processing time: {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    main()