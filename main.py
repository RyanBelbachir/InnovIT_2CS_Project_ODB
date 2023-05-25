from fastapi import FastAPI
from prisma import Prisma
import uvicorn


from routes.sensors import router as router_sensors


app = FastAPI()

prisma = Prisma()


app.include_router(router_sensors)



@app.get("/")
async def read_root():
    return {"Hello": "World"}


