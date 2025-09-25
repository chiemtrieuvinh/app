from routers import user, task, company, auth
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

app.include_router(user.router)
app.include_router(task.router)
app.include_router(company.router)
app.include_router(auth.router)

@app.get("/")
async def health_check():
    return {"message": "API service is up and running"}