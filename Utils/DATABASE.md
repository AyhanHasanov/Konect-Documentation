# Database Utility
This file defines 2 classes - `Database` and `PoolConnection`

## Database class: 
The class is responsible for initializing and managing a pooled set of secure connections to a Snowflake database using key-pair authentication.

There's one class method `initialise` that is responsible for setting up the connection pool.
Workflow:
1. Reading the private key from e `.env` file.
2. Parses the key into a `DER`	using cryptography.
3. Establishes a connection with Snowflake
```python
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER", "svc_snowflake_usr_dev"), ...
)
``` 
4. A **thread-safe queue-based connection pool** is created.    
-   It reuses connections instead of creating a new one for each request.
```python
cls.connection_pool = pool.QueuePool(
    get_conn, max_overflow=1, pool_size=5, timeout=60, recycle=300
)
```

## PoolConnection Class
PoolConnection is a context manager (via ``__enter__`` and ``__exit__`` methods) that provides safe, reusable access to a database connection from the previously defined connection pool.

It ensures:
- Connections are properly acquired and released
- Connections are re-initialized if the pool fails
- All changes are committed when the block finishes

####   `__enter__(self)`
```python 
def  __enter__(self): try:
        self.connection = Database.connection_pool.connect() except Exception as e:
        Database.initialise()
        self.connection = Database.connection_pool.connect()
```

-   Acquires a connection from the pool.
-   If the pool is broken (e.g., expired tokens or app start), it reinitializes the pool and tries again.
-   Returns the connection to be used in a `with` block.

#### `__exit__(self, exc_type, exc_val, exc_tb)`

```python
def  __exit__(self, exc_type, exc_val, exc_tb):
    self.connection.commit()
    self.connection.close()
```
-   Called automatically when exiting the `with` block.
-   Commits the transaction (ensuring changes are saved).
-   Closes the connection (returns it to the pool).