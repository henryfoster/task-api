from fastapi import FastAPI

from app.routers.task_endpoints import router as task_router

app = FastAPI()
app.include_router(task_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World!"}
