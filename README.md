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

### Assessment Evidence

Task 2 provides the required evidence through:

- working evidence-filter implementation
- documented run command
- happy-path example
- rejection paths for internal and unverified evidence
- automated success and failure tests
- saved execution output
- saved test output
- input validation
- traceable evidence sources and flags
- accepted/rejected evidence counts
- processing-time measurement

### Guardrails

Validation is applied because it directly relates to the evidence-filter operation.

Retry, timeout, and step-limit controls are not added because this task does not perform external API calls, retryable operations, or long-running execution steps.