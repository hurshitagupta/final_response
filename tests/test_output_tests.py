import pytest

from output_tests import FinalOutput, check_final_output


def test_valid_success_output():
    output = FinalOutput(answer="The requested report has been generated successfully.", status="success", completed_action="Generated the requested report.", warnings=[], next_action=None)

    assert check_final_output(output) is True


def test_empty_answer_is_rejected():
    output = FinalOutput(answer="", status="success", completed_action="Generated the report.", warnings=[], next_action=None)

    with pytest.raises(ValueError, match="Final answer cannot be empty"):
        check_final_output(output)


def test_invalid_status_is_rejected():
    output = FinalOutput(answer="Report ready.", status="unknown", completed_action="Generated the report.", warnings=[], next_action=None)

    with pytest.raises(ValueError, match="Invalid final output status"):
        check_final_output(output)


def test_failure_requires_next_action():
    output = FinalOutput(answer="Unable to complete the report.", status="failure", completed_action="Checked available report data.", warnings=["Required data is missing."], next_action=None)

    with pytest.raises(ValueError, match="Failure output must include a next action"):
        check_final_output(output)


def test_partial_output_requires_warning():
    output = FinalOutput(answer="Part of the report was generated.", status="partial", completed_action="Generated available sections.", warnings=[], next_action="Provide the missing data.")

    with pytest.raises(ValueError, match="Partial output must include a warning"):
        check_final_output(output)


def test_internal_content_is_rejected():
    output = FinalOutput(answer="Report generated. INTERNAL NOTE: check record 25.", status="success", completed_action="Generated the requested report.", warnings=[], next_action=None)

    with pytest.raises(ValueError, match="Final output contains blocked internal content"):
        check_final_output(output)