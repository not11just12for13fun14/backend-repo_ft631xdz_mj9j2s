import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Dish, Reservation, BocconeBuild

app = FastAPI(title="Boccone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helpers
class ObjectIdStr(BaseModel):
    id: str


def collection(name: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    return db[name]


@app.get("/")
def root():
    return {"message": "Boccone backend is running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected"
            response["connection_status"] = "Connected"
            response["collections"] = db.list_collection_names()
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# Menu endpoints
@app.post("/dishes", response_model=dict)
def create_dish(dish: Dish):
    dish_id = create_document("dish", dish)
    return {"id": dish_id}


@app.get("/dishes", response_model=List[dict])
def list_dishes(tag: Optional[str] = None, featured: Optional[bool] = None):
    query = {}
    if tag:
        query["tags"] = tag
    if featured is not None:
        query["featured"] = featured
    docs = get_documents("dish", query)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


# Reservations
@app.post("/reservations", response_model=dict)
def create_reservation(reservation: Reservation):
    res_id = create_document("reservation", reservation)
    return {"id": res_id}


# Boccone builds
@app.post("/bocconi", response_model=dict)
def save_boccone_build(build: BocconeBuild):
    build_id = create_document("bocconebuild", build)
    return {"id": build_id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
