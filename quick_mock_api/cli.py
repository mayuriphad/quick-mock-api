import argparse
import os
import uvicorn
from .server import create_app

def main():
    parser = argparse.ArgumentParser(description="Start a zero-config REST API mock server.")
    parser.add_argument("source", help="Path to the JSON database file (e.g., db.json)")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on (default: 8000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind the server to (default: 127.0.0.1)")

    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"Error: Database file '{args.source}' not found.")
        print(f"Creating a template file at '{args.source}'...")
        with open(args.source, "w") as f:
            f.write('{"posts": [{"id": 1, "title": "hello world"}]}')
        print("Template created.")

    app = create_app(args.source)
    print(f"Starting Quick Mock API server on http://{args.host}:{args.port}")
    print(f"Using database: {args.source}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

if __name__ == "__main__":
    main()
