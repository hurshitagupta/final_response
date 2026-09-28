import pytest

from response_schema import build_response


def test_success_response():
    response = build_response(result="Report generated successfully.", status="success", completed_action="Generated the requested report.")

    assert response.status == "success"
    assert response.answer == "Report generated successfully."
    assert response.completed_action == "Generated the requested report."
    assert response.warnings == []
    assert response.next_action is None


def test_failure_response():
    response = build_response(result="Required data was unavailable.", status="failure", completed_action="Checked available report data.", warning="Required data is missing.", next_action="Provide the missing data.")

    assert response.status == "failure"
    assert response.answer.startswith("Unable to complete:")
    assert "Required data is missing." in response.warnings
    assert response.next_action == "Provide the missing data."


def test_empty_result_is_rejected():
    with pytest.raises(ValueError, match="Result cannot be empty"):
        build_response(result="", status="success", completed_action="Generate report.")


def test_invalid_status_is_rejected():
    with pytest.raises(ValueError, match="Invalid response status"):
        build_response(result="Report ready.", status="unknown", completed_action="Generated report.")