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

### Assessment Evidence

Task 1 provides the required assessment evidence through:

- working response-schema implementation
- documented run command
- happy-path demonstration
- failure/rejection demonstration
- input and output validation
- automated success and failure tests
- saved execution output
- saved test output
- response count and processing-time measurement
- traceable response fields showing status, completed action, warnings, and next action

### Guardrails

No retry, timeout, or step-limit mechanism is added to this task because the response-schema operation contains no external call, retryable operation, or execution loop.

Validation is implemented because it directly applies to the response contract.
