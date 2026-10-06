# quick-mock-api

A zero-config REST API mock server for Python. Get a full fake REST API with zero coding in less than 30 seconds (seriously), just by providing a JSON file. Inspired by the legendary Node.js `json-server`.

## Installation

```bash
pip install quick-mock-api
```

## Usage

Create a `db.json` file with some data:

```json
{
  "posts": [
    { "id": 1, "title": "hello world" }
  ],
  "comments": [
    { "id": 1, "body": "some comment", "postId": 1 }
  ]
}
```

Start the API:

```bash
mock-api db.json
```

Now you have a full fake REST API running at `http://localhost:8000`!
