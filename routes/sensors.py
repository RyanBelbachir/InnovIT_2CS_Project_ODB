from fastapi import APIRouter
from prisma import Prisma
from pydantic import BaseModel
from datetime import datetime
router = APIRouter()

prisma = Prisma()

@router.on_event("startup")
async def startup():
    await prisma.connect()
@router.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


class Category(BaseModel):
    id : int
    sensor : str

class SensorsData(BaseModel):
    id : int
    idDistr : int
    idSensor : int 
    value : str
    date : str


@router.get('/ODB/categories')
async def get_categories():
    category_list = await prisma.categorysensors.find_many(
    )

    return category_list

@router.post('/ODB/sensors/data')
async def addDataSensors(sensors: list[dict]):
    today_date = datetime.now()
    formatted_date = today_date.strftime("%d-%m-%Y %H:%M:%S")
    for sensor in sensors:
        sensorvalue = await prisma.sensors.create(
        data = {
            'idDistr': sensor['idDistr'],
            'idSensor': sensor['idSensor'],
            'value' : sensor['value'],
            'date' : formatted_date

        },
    )
    return {"message": "Data inserted successfully."}