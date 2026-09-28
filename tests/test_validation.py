import pytest

from validation import ResponseData, validate_response


def test_valid_success_response():
    response = ResponseData(answer="Report generated successfully.", status="success", completed_action="Generated the requested report.", warnings=[], next_action=None)

    assert validate_response(response) is True


def test_failure_requires_next_action():
    response = ResponseData(answer="Unable to complete the report.", status="failure", completed_action="Checked report data.", warnings=["Required data is missing."], next_action=None)

    with pytest.raises(ValueError, match="Failure response must include a next action"):
        validate_response(response)


def test_empty_answer_is_rejected():
    response = ResponseData(answer="", status="success", completed_action="Generated report.", warnings=[], next_action=None)

    with pytest.raises(ValueError, match="Answer cannot be empty"):
        validate_response(response)


def test_invalid_status_is_rejected():
    response = ResponseData(answer="Report ready.", status="unknown", completed_action="Generated report.", warnings=[], next_action=None)

    with pytest.raises(ValueError, match="Invalid response status"):
        validate_response(response)


def test_partial_response_requires_warning():
    response = ResponseData(answer="Part of the report was generated.", status="partial", completed_action="Generated available report sections.", warnings=[], next_action="Provide the missing data.")

    with pytest.raises(ValueError, match="Partial response must include at least one warning"):
        validate_response(response)