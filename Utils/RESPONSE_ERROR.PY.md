## Purpose

Provides a **custom exception class** to simplify consistent error reporting in API responses.

This helps frontend developers receive clear, categorized messages.

---

## Class: `ApiException(Exception)`

### Signature:

```python
ApiException(error_group, error_type, error_message)
```

### Attributes:

- `error_group`: Logical module (e.g., "ROI", "PREDICTION")

- `error_type`: Error class (e.g., "BAD_INPUT", "PROCESSING", "NOT_FOUND")

- `error_message`: User-friendly or developer-facing error detail

### Behavior:

- Can be raised inside `try/except` blocks across the project.

- Typically caught at the Flask error handler level to return structured JSON responses like:


```json
{
  "errorGroup": "ROI",
  "errorType": "BAD_INPUT",
  "errorMessage": "Missing projectStartDate in request."
}
```

## Used In:

- `roi.py`, `demand.py`, and others for safe error handling

- Consistent API error responses for debugging and frontend display