# quick-mock-api

[![PyPI](https://img.shields.io/pypi/v/quick-mock-api.svg)](https://pypi.org/project/quick-mock-api/)
[![Downloads](https://img.shields.io/pypi/dm/quick-mock-api.svg)](https://pypistats.org/packages/quick-mock-api)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

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

## Advanced Features

### Filtering
You can filter results using query parameters:
```bash
GET /posts?title=hello world
```

### Sorting
Use `_sort` and `_order` (asc or desc) to sort results:
```bash
GET /posts?_sort=id&_order=desc
```

### Pagination
Use `_page` and `_limit` to paginate results:
```bash
GET /posts?_page=1&_limit=5
```

## 👤 Author
Built with ❤️ by **mayuriphad** (mayuriphad656@gmail.com).
