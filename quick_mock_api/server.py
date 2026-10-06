import json
import os
from fastapi import FastAPI, HTTPException, Request, Response

def create_app(db_path: str) -> FastAPI:
    app = FastAPI(title="Quick Mock API", description="Zero-config JSON-based REST API")
    
    def read_db():
        with open(db_path, "r") as f:
            return json.load(f)
            
    def write_db(data):
        with open(db_path, "w") as f:
            json.dump(data, f, indent=2)

    @app.api_route("/{table_name}", methods=["GET", "POST"])
    async def handle_collection(table_name: str, request: Request):
        db_data = read_db()
        if table_name not in db_data:
            db_data[table_name] = []
            
        table = db_data[table_name]
        
        if request.method == "GET":
            results = list(table)
            params = dict(request.query_params)
            
            for key, value in params.items():
                if not key.startswith("_"):
                    results = [r for r in results if str(r.get(key)) == str(value)]
                    
            sort_by = params.get("_sort")
            if sort_by:
                order = params.get("_order", "asc")
                results = sorted(results, key=lambda x: x.get(sort_by, ""), reverse=(order.lower() == "desc"))
                
            page = int(params.get("_page", 1))
            limit = int(params.get("_limit", len(results) if results else 10))
            if "_page" in params or "_limit" in params:
                start = (page - 1) * limit
                end = start + limit
                results = results[start:end]

            return results
            
        elif request.method == "POST":
            try:
                data = await request.json()
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid JSON body")
            
            if "id" not in data:
                max_id = max([r.get("id", 0) for r in table]) if table else 0
                data["id"] = max_id + 1
                
            table.append(data)
            write_db(db_data)
            return data

    @app.api_route("/{table_name}/{item_id}", methods=["GET", "PUT", "PATCH", "DELETE"])
    async def handle_item(table_name: str, item_id: int, request: Request):
        db_data = read_db()
        if table_name not in db_data:
            raise HTTPException(status_code=404, detail="Table not found")
            
        table = db_data[table_name]
        
        item_index = next((i for i, item in enumerate(table) if str(item.get("id")) == str(item_id)), None)
        if item_index is None:
            raise HTTPException(status_code=404, detail="Item not found")
            
        item = table[item_index]

        if request.method == "GET":
            return item
            
        elif request.method == "PUT" or request.method == "PATCH":
            try:
                data = await request.json()
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid JSON body")
            
            if request.method == "PUT":
                data["id"] = item.get("id")
                table[item_index] = data
            else: # PATCH
                new_data = dict(item)
                new_data.update(data)
                new_data["id"] = item.get("id")
                table[item_index] = new_data
                
            write_db(db_data)
            return table[item_index]
                
        elif request.method == "DELETE":
            table.pop(item_index)
            write_db(db_data)
            return Response(status_code=204)

    return app
