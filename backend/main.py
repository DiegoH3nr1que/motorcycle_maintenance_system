from fastapi import FastAPI
from database.config import init_db
from routers import maintenance, motorcycle
app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(motorcycle.router, prefix="/api")
app.include_router(maintenance.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
