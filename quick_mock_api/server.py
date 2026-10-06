from fastapi import FastAPI, HTTPException, Request, Response
from tinydb import TinyDB, Query

def create_app(db_path: str) -> FastAPI:
    app = FastAPI(title="Quick Mock API", description="Zero-config JSON-based REST API")
    db = TinyDB(db_path)
    
    @app.api_route("/{table_name}", methods=["GET", "POST"])
    async def handle_collection(table_name: str, request: Request):
        table = db.table(table_name)
        
        if request.method == "GET":
            results = table.all()
            
            # Query parameters
            params = dict(request.query_params)
            
            # 1. Filtering (any param not starting with _)
            for key, value in params.items():
                if not key.startswith("_"):
                    # Basic exact match filtering
                    results = [r for r in results if str(r.get(key)) == str(value)]
                    
            # 2. Sorting (_sort, _order)
            sort_by = params.get("_sort")
            if sort_by:
                order = params.get("_order", "asc")
                results = sorted(results, key=lambda x: x.get(sort_by, ""), reverse=(order.lower() == "desc"))
                
            # 3. Pagination (_page, _limit)
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
            
            # Ensure an ID exists
            if "id" not in data:
                all_records = table.all()
                max_id = max([r.get("id", 0) for r in all_records]) if all_records else 0
                data["id"] = max_id + 1
                
            table.insert(data)
            return data

    @app.api_route("/{table_name}/{item_id}", methods=["GET", "PUT", "PATCH", "DELETE"])
    async def handle_item(table_name: str, item_id: int, request: Request):
        table = db.table(table_name)
        ItemQuery = Query()
        
        item = table.get(ItemQuery.id == item_id)
        if not item:
            # Fallback to string matching in case ID was passed as string
            item = table.get(ItemQuery.id == str(item_id))
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")

        if request.method == "GET":
            return item
            
        elif request.method == "PUT" or request.method == "PATCH":
            try:
                data = await request.json()
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid JSON body")
            
            if request.method == "PUT":
                data["id"] = item.get("id")
                table.update(data, ItemQuery.id == item.get("id"))
                return data
            else: # PATCH
                new_data = dict(item)
                new_data.update(data)
                new_data["id"] = item.get("id")
                table.update(new_data, ItemQuery.id == item.get("id"))
                return new_data
                
        elif request.method == "DELETE":
            table.remove(ItemQuery.id == item.get("id"))
            return Response(status_code=204)

    return app
