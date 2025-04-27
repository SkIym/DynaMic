## Running the Server

1. Navigate to the `/src` directory:
   ```bash
   cd src

2. Then run:
    ```bash
    uvicorn app:app

    ```
    To enable auto-reload during development:
    ```bash
    uvicorn app:app --reload

    ```

## Testing the APIs

1. Once the server is running, access the API documentation or test the endpoints at:
    ```bash
    http://127.0.0.1:8000/docs