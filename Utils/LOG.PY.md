# Log Util

This document explains the logic inside the utility file:  
**`utils/log.py`**

It is intended to be used for **logging endpoint activity** or general debug messages into a PostgreSQL `logs` table.

---

## Purpose

This utility provides a simple method to **store messages in the database**, primarily for tracking usage, debugging, or auditing purposes.

Although it is **not currently used in the project**, the function is built to write entries into a `logs` table with two fields:

- `ID` — currently hardcoded as `'DDD'`
    
- `ENDPOINT` — a string message passed at runtime
    

---

## Function: `db_log(message)`

Inserts a log entry into the database using a connection from the shared **`PoolConnection`** pool.

### Behavior:

- Opens a connection using `PoolConnection` context manager

- Executes an `INSERT INTO logs(ID, ENDPOINT)` query

- Commits the transaction immediately

### Example:

```python
db_log("/api/v1/roi")  # → Logs the message "/api/v1/roi" with ID 'DDD'
```

## Used In

- _Currently unused_ — this utility is available for future logging needs

- Can be used to track API hits, performance issues, or custom debug checkpoints during runtime