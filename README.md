## Task 1 — Response Schema

### Objective

This task implements a structured final-response schema so that the system returns a consistent response instead of an unstructured string.

The response communicates:

- the final answer
- completion status
- what action was completed
- warnings or limitations
- the next action when additional work is required

This supports the assessment requirement that a final response should answer the user's goal, explain what was done, disclose important limitations, and make unresolved work actionable.

---

### Implementation

The `FinalResponse` dataclass defines the output contract:

```python
@dataclass
class FinalResponse:
    answer: str
    status: Status
    completed_action: str
    warnings: list[str]
    next_action: str | None
```

The `build_response()` function validates the provided result and status before creating the final response.

Supported statuses are:

```text
success
failure
partial
```

A successful response returns the result directly.

A failure response clearly states that the request could not be completed and can include:

- a warning explaining the limitation
- a next action explaining what the user can do next

---

### Happy Path

The happy-path example generates a successful final response. The response contains no warning or unresolved next action.

---

### Failure Path

The failure example demonstrates how the response behaves when required information is unavailable.

Example:

```text
Unable to complete: Required data was unavailable.
```

The user is also told that the missing data should be provided before retrying.

---

### Validation

The implementation validates the response before returning it.

The following invalid cases are rejected:

- empty result
- unsupported response status

For example, an empty result raises:

```text
ValueError: Result cannot be empty.
```

This prevents an invalid or incomplete final response from being returned.

---

### Measurement

The implementation records:

- number of responses created
- response-processing time in milliseconds

Example:

```text
Responses created: 2
Processing time: 0.10 ms
```

The exact processing time may vary between runs.

---

### Run Command

Run Task 1 from the project root:

```powershell
python response_schema.py
```
---

### Automated Tests

Run the Task 1 tests using:

```powershell
pytest tests/test_response_schema.py -v
```

The tests verify:

- successful response creation
- failure response creation
- empty result rejection
- invalid status rejection

---

### Guardrails

No retry, timeout, or step-limit mechanism is added to this task because the response-schema operation contains no external call, retryable operation, or execution loop.

Validation is implemented because it directly applies to the response contract.

---

## Task 2 — Evidence Filter

### Objective

This task implements an evidence-filtering step before information is included in the final response.

The filter ensures that only verified, external evidence is allowed through, while internal notes and unverified information are excluded.

This supports the assessment objectives around:

- internal versus external state
- synthesis
- safe final-response construction
- traceable evidence handling

---

### Implementation

The `Evidence` dataclass defines the structure of each evidence item:

```python
@dataclass
class Evidence:
    content: str
    source: str
    verified: bool
    internal: bool = False
```

Each evidence item contains:

- `content` — the information being considered
- `source` — where the evidence came from
- `verified` — whether the evidence is considered valid
- `internal` — whether the information is internal-only

The `filter_evidence()` function accepts a list of evidence items and returns only the items that are safe to use in the final response.

Evidence is accepted only when:

```text
verified = True
internal = False
```

Internal or unverified evidence is excluded.

---

### Happy Path

The happy-path example uses verified, external evidence.

Because it is verified and not internal, it is accepted by the filter.

---

### Failure / Rejection Path

The implementation demonstrates two rejection cases.

#### Unverified Evidence

Example:

```text
The report may contain 30 records.
```

This evidence is marked:

```text
verified = False
```

It is rejected because unverified information should not be used in the final response.

---

### Validation

The function validates that the evidence input is provided as a list.

Invalid input such as:

```text
"invalid input"
```

is rejected with:

```text
ValueError: Evidence must be provided as a list.
```

The function also validates that each item follows the `Evidence` schema.

This prevents incorrectly structured evidence from being processed.

---

### Traceability

Each evidence item keeps its source and verification state.

During execution, the program prints:

- evidence content
- evidence source
- verification status
- internal/external status

This makes it possible to follow which evidence was received and why it was accepted or rejected.

---

### Measurement

The implementation records:

- total evidence items received
- total evidence items accepted
- total evidence items rejected
- processing time in milliseconds

The processing time may vary between runs.

---

### Run Command

Run Task 2 from the project root:

```powershell
python evidence_filter.py
```
---

### Automated Tests

Run the Task 2 tests using:

```powershell
pytest tests/test_evidence_filter.py -v
```

The tests verify:

- verified external evidence is accepted
- unverified evidence is rejected
- internal evidence is rejected
- invalid input is rejected

---

### Guardrails

Validation is applied because it directly relates to the evidence-filter operation.

Retry, timeout, and step-limit controls are not added because this task does not perform external API calls, retryable operations, or long-running execution steps.

---

## Task 3 — Validation

### Objective

This task implements validation for the final response before it is returned to the user.

The validation ensures that the response:

- contains a non-empty answer
- uses a supported status
- states what action was completed
- includes an actionable next step when the response fails
- includes a warning when the response is only partially complete

This supports the assessment requirement that final responses should be complete, structured, and useful to the user.

---

### Implementation

The `ResponseData` dataclass defines the response structure:

```python
@dataclass
class ResponseData:
    answer: str
    status: str
    completed_action: str
    warnings: list[str]
    next_action: str | None
```

The `validate_response()` function checks whether the response satisfies the expected output contract before it can be returned.
---

### Validation Rules

The following checks are implemented.

#### Answer Validation

The response must contain a non-empty answer.

An empty answer is rejected with:

```text
ValueError: Answer cannot be empty.
```

#### Status Validation

Only the following statuses are accepted:

```text
success
failure
partial
```

Any unsupported status is rejected.

#### Completed Action Validation

The response must explain what action was performed.

An empty `completed_action` is rejected.

#### Failure Response Validation

A response with:

```text
status = failure
```

must include a `next_action`.

This ensures that a failed request does not leave the user without guidance about what to do next.

#### Partial Response Validation

A response with:

```text
status = partial
```

must contain at least one warning.

This ensures that important limitations are clearly disclosed.

---

### Happy Path

The happy-path example uses a valid successful response

The response satisfies all required validation checks and returns.
---

### Failure / Rejection Path

The rejection example uses a response with:

```text
status = failure
```

but does not provide a next action.

The response is rejected with:

```text
Failure response must include a next action.
```

This demonstrates that incomplete failure responses are prevented from reaching the user.

---

### Traceability

The execution output shows:

- the response being validated
- whether the response is accepted
- why an invalid response is rejected
- counts of valid and rejected responses

This makes the validation decision observable and reviewable.

---

### Measurement

The implementation records:

- total responses checked
- valid responses
- rejected responses
- processing time in milliseconds

---

### Run Command

Run Task 3 from the project root:

```powershell
python validation.py
```
---

### Automated Tests

Run the Task 3 tests using:

```powershell
pytest tests/test_validation.py -v
```

The tests verify:

- a valid success response is accepted
- a failure response without a next action is rejected
- an empty answer is rejected
- an invalid status is rejected
- a partial response without a warning is rejected

---

### Guardrails

Validation is the main guardrail used in this task because it directly applies to the final-response contract.

Retry, timeout, and step-limit controls are not added because this task performs only local validation and does not contain external calls, retryable operations, or long-running execution loops.

---

## Task 4 — Redaction

### Objective

This task implements redaction before the final response is shown to the user.

The purpose is to prevent sensitive information from appearing in the external response.

The implementation currently redacts:

- email addresses
- phone numbers
- API-key-like values

This supports the assessment objective of keeping internal or sensitive information separate from the user-facing final response.

---

### Implementation

The `redact_sensitive_data()` function checks the response text for sensitive patterns.

The implementation uses regular expressions for:

```text
EMAIL_PATTERN
PHONE_PATTERN
API_KEY_PATTERN
```

When a sensitive value is found, it is replaced with a safe placeholder.

---

### Happy Path

The happy-path example uses normal text without any sensitive information:

```text
Report generated successfully for the customer.
```

Since no sensitive value is present, the output remains unchanged.

This demonstrates that normal final-response content is not modified unnecessarily.

---

### Sensitive Data Path

The implementation also demonstrates redaction using text containing:

- an email address
- a phone number
- an API-key-like value

---

### Failure / Rejection Path

The function validates its input before redaction.

An empty string is rejected:

```text
ValueError: Input text cannot be empty.
```

A non-string input is also rejected:

```text
ValueError: Input must be a string.
```

This prevents invalid response data from being processed.

---

### Validation and Safe Boundary

The redaction layer acts as a boundary between internal data and the external final response.

Before text can be returned to the user, the function checks for sensitive values and replaces them with safe placeholders.

This helps prevent accidental exposure of information that should not appear in the final response.

---

### Traceability

The execution output shows:

- the original safe text
- the unchanged safe result
- the original sensitive text
- the redacted result
- rejected invalid input
- number of values redacted

This makes the redaction behavior visible and reviewable.

---

### Measurement

The implementation records:

- number of sensitive values redacted
- number of rejected inputs
- processing time in milliseconds


### Run Command

Run Task 4 from the project root:

```powershell
python redaction.py
```

---

### Automated Tests

Run the Task 4 tests using:

```powershell
pytest tests/test_redaction.py -v
```

The tests verify:

- safe text remains unchanged
- email addresses are redacted
- phone numbers are redacted
- API-key-like values are redacted
- empty input is rejected
- non-string input is rejected

---

### Guardrails

Validation and redaction are applied because they directly relate to this task.

Retry, timeout, and step-limit controls are not added because this task performs only local text processing and does not contain external calls, retryable operations, or long-running execution loops.

---

## Task 5 — Output Tests

### Objective

This task implements final output tests before a response is returned to the user.

The purpose is to verify that the completed response satisfies the expected output contract and does not expose incomplete or internal information.

The final output is checked for:

- non-empty answer
- valid completion status
- completed action
- actionable next step for failed responses
- warning for partially completed responses
- blocked internal content

This provides a final quality check on the user-facing response.

---

### Implementation

The `FinalOutput` dataclass defines the expected final-response structure:

```python
@dataclass
class FinalOutput:
    answer: str
    status: str
    completed_action: str
    warnings: list[str]
    next_action: str | None
```

The `check_final_output()` function verifies the complete response before it is returned.

---

### Output Checks

The implementation verifies that the final answer is not empty.

It also ensures that the response uses a supported status and contains a description of the completed action.

For failure responses, a `next_action` is required so that unresolved work remains actionable.

For partial responses, at least one warning must be present so that limitations are clearly disclosed.

The implementation also checks for internal markers such as:

```text
INTERNAL NOTE:
DEBUG:
SYSTEM:
TOOL_CALL:
```

These markers are rejected if they appear in the final user-facing response.

---

### Happy Path

The happy-path example creates a valid successful response.

---

### Failure / Rejection Path

The rejection example contains internal information inside the final answer.

---

### Validation

The implementation rejects:

- empty final answers
- unsupported statuses
- missing completed actions
- failed responses without a next action
- partial responses without warnings
- final responses containing blocked internal markers

This ensures that only complete and appropriate outputs can pass the final check.

---

### Traceability

The execution output shows:

- the valid output being checked
- whether the valid output passes
- the rejected output
- the reason for rejection
- number of valid and rejected outputs

This makes the final output decision observable and reviewable.

---

### Measurement

The implementation records:

- total outputs checked
- valid outputs
- rejected outputs
- processing time in milliseconds

---

### Run Command

Run Task 5 from the project root:

```powershell
python output_tests.py
```

---

### Automated Tests

Run the Task 5 tests using:

```powershell
pytest tests/test_output_tests.py -v
```

The automated tests verify:

- valid successful output passes
- empty answer is rejected
- invalid status is rejected
- failed output without a next action is rejected
- partial output without a warning is rejected
- internal content is rejected

---

### Guardrails

Output validation and internal-content checks are applied because they directly relate to the final response.

Retry, timeout, and step-limit controls are not added because this task performs local output validation and does not include external calls, retries, or long-running operations.