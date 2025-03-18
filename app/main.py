from fastapi import FastAPI
import uvicorn
import json

from .database import engine 
from . import models
from .routers import post, user, auth, vote
from .config import Settings

settings = Settings()



with open("config.json") as config_file:
    config = json.load(config_file)

host_vm = config["application"]["host"]
port_vm = config["application"]["port"]

""" Useless if using alembic"""
## models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# @app.get("/", include_in_schema=False)
# async def redirect_to_docs():
#     return RedirectResponse(url="/docs")

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host=host_vm, port=port_vm)
    ## OR
    ## >>> uvicorn main:app --host 172.25.13.145 --port 8080
