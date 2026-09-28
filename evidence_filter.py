from dataclasses import dataclass
import time


@dataclass
class Evidence:
    content: str
    source: str
    verified: bool
    internal: bool = False


def filter_evidence(evidence_items: list[Evidence]) -> list[Evidence]:
    if not isinstance(evidence_items, list):
        raise ValueError("Evidence must be provided as a list.")

    accepted = []

    for item in evidence_items:
        if not isinstance(item, Evidence):
            raise ValueError("Each evidence item must use the Evidence schema.")

        if not item.content.strip():
            continue

        if item.internal:
            continue

        if not item.verified:
            continue

        accepted.append(item)

    return accepted


def main():
    start_time = time.perf_counter()

    print("=== EVIDENCE FILTER ===\n")

    evidence_items = [
        Evidence(content="The report contains 25 completed records.", source="report_data", verified=True),
        Evidence(content="Maybe the user prefers a shorter report.", source="internal_note", verified=True, internal=True),
        Evidence(content="The report may contain 30 records.", source="unverified_source", verified=False),
    ]

    print("Input Evidence:")
    for item in evidence_items:
        print(f"- {item.content} "
            f"| source={item.source} "
            f"| verified={item.verified} "
            f"| internal={item.internal}"
        )

    filtered = filter_evidence(evidence_items)

    print("\nAccepted Evidence:")

    for item in filtered:
        print(f"- {item.content} | source={item.source}")

    rejected_count = len(evidence_items) - len(filtered)

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print("\n=== MEASUREMENT ===")
    print(f"Evidence received: {len(evidence_items)}")
    print(f"Evidence accepted: {len(filtered)}")
    print(f"Evidence rejected: {rejected_count}")
    print(f"Processing time: {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    main()