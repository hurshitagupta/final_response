import pytest

from evidence_filter import Evidence, filter_evidence


def test_verified_external_evidence_is_accepted():
    evidence = [Evidence(content="The report contains 25 completed records.", source="report_data", verified=True)]

    result = filter_evidence(evidence)

    assert len(result) == 1
    assert result[0].content == "The report contains 25 completed records."
    assert result[0].source == "report_data"


def test_unverified_evidence_is_rejected():
    evidence = [Evidence(content="The report may contain 30 records.", source="unverified_source", verified=False)]

    result = filter_evidence(evidence)

    assert result == []


def test_internal_evidence_is_rejected():
    evidence = [Evidence(content="Internal reasoning about the response.", source="internal_note", verified=True, internal=True)]

    result = filter_evidence(evidence)

    assert result == []


def test_invalid_input_is_rejected():
    with pytest.raises(ValueError, match="Evidence must be provided as a list"):
        filter_evidence("invalid input")