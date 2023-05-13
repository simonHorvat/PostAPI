import uvicorn
from app.main import app
from database.database import Base, engine
from database.load_data import load_toy_data


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    load_toy_data()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
