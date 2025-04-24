# HTTP to Google Cloud Pub/Sub Bridge

This project provides a simple HTTP server that listens for POST requests. When it receives a request with a JSON body containing `content` and `pubsub_name` fields, it publishes the `content` to the specified Google Cloud Pub/Sub topic within the same Google Cloud project.

## Overview

The application consists of a Python script (`app.py`) and a Dockerfile for containerization, making it easy to deploy on platforms like Cloudron.

**Key Features:**

* Accepts HTTP POST requests on port 8080.
* Expects a JSON request body with the following structure:
    ```json
    {
      "content": "The message to publish to Pub/Sub",
      "pubsub_name": "your-pubsub-topic-name"
    }
    ```
* Publishes the value of the `content` field to the Pub/Sub topic specified in the `pubsub_name` field.
* Uses the `GOOGLE_CLOUD_PROJECT` environment variable to determine the Google Cloud project ID.
* Provides basic error handling for missing fields, invalid JSON, and Pub/Sub publishing failures.

## Files

* **`app.py`**: The main Python script containing the HTTP server logic and Pub/Sub publishing functionality.
* **`Dockerfile`**: The Dockerfile used to build a container image for the application.
* **`requirements.txt`**: Lists the Python dependencies required by the application.
* **`README.md`**: This file, providing an overview and instructions for the project.

## Prerequisites

* **Google Cloud Account:** You need a Google Cloud account with the Pub/Sub API enabled.
* **Google Cloud Project ID:** You'll need your Google Cloud Project ID.
* **Pub/Sub Topic(s):** Ensure that the Pub/Sub topic(s) you intend to publish to exist in your Google Cloud project.
* **Cloudron Environment (Optional but Recommended):** These instructions are tailored for deployment on Cloudron.
* **Docker (for local building):** If you want to build the Docker image locally.
* **Python 3.9 or higher (for local testing):** If you want to run the Python script directly.
* **`pip` (Python package installer):** To install the required Python libraries.

## Setup and Deployment on Cloudron

1.  **Create Project Files:** Create the following files in a directory for your project:
    * `app.py` (the Python code provided)
    * `Dockerfile` (the Dockerfile provided)
    * `requirements.txt` (containing `google-cloud-pubsub`)
    * `manifest.json` (a Cloudron manifest file - see example below)

2.  **`requirements.txt`:**
    ```
    google-cloud-pubsub
    ```

3.  **`manifest.json` (Example):**
    ```json
    {
      "id": "your-app-id",
      "version": "0.0.1",
      "schema": {
        "type": "object",
        "properties": {}
      },
      "ports": {
        "http": {
          "protocol": "http",
          "port": 8080
        }
      }
    }
    ```
    * Replace `"your-app-id"` with a unique identifier for your app.

4.  **Build and Deploy on Cloudron:**
    * Use the Cloudron CLI or the web dashboard to build and install your custom app using the provided `Dockerfile` and `manifest.json`.
    * During the app configuration on Cloudron, **set the environment variable `GOOGLE_CLOUD_PROJECT` to your Google Cloud Project ID.**

5.  **Access the Endpoint:** Once the app is running on Cloudron, you can send HTTP POST requests to its assigned URL and port (typically port 8080).

## Docker Instructions (for local building)

1.  **Save Files:** Ensure `app.py`, `Dockerfile`, and `requirements.txt` are in the same directory.
2.  **Build Image:** Open a terminal in that directory and run:
    ```bash
    docker build -t your-app-name .
    ```
    (Replace `your-app-name` with a name for your image).
3.  **Run Container (for testing):**
    ```bash
    docker run -p 8080:8080 -e GOOGLE_CLOUD_PROJECT="YOUR_GOOGLE_CLOUD_PROJECT_ID" your-app-name
    ```
    (Replace `"YOUR_GOOGLE_CLOUD_PROJECT_ID"` with your actual project ID).

## Usage

Send an HTTP POST request to the server's endpoint (e.g., `http://your-app-domain.com:8080` on Cloudron) with a JSON body like this:

```json
{
  "content": "This is the message content.",
  "pubsub_name": "your-pubsub-topic"
}
```

You can use tools like `curl` to send the request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"content": "Hello from the HTTP server!", "pubsub_name": "my-topic"}' [http://your-app-domain.com:8080](http://your-app-domain.com:8080)
```

## Important Considerations

* **Google Cloud Authentication:** The container running this code needs the necessary permissions to publish to Google Cloud Pub/Sub. In a Cloudron environment, this might be handled automatically through the underlying infrastructure (e.g., if running on Google Cloud Run) or you might need to configure Workload Identity or other authentication mechanisms. Ensure the service account associated with your Cloudron instance or the container has the `roles/pubsub.publisher` role on your project or the specific Pub/Sub topics. Consult the Cloudron documentation for best practices regarding Google Cloud service account integration.
* **Error Handling:** The provided code includes basic error handling. You might want to enhance it to include more robust logging and error reporting.
* **Security:** Consider security implications when exposing an HTTP endpoint. Ensure appropriate network policies and security measures are in place.
* **Scalability and Reliability:** For production environments, consider deploying this application in a more scalable and resilient manner, potentially using managed services.

This README provides a comprehensive guide to understanding and deploying the HTTP to Google Cloud Pub/Sub bridge application. Remember to configure the `GOOGLE_CLOUD_PROJECT` environment variable correctly for your Cloudron deployment.
