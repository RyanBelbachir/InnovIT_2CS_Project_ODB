from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

# Configure the database connection
engine = create_engine(
    "mysql+mysqlconnector://innovit_user:innovit_pwd@mysql-innovit.alwaysdata.net:3306/innovit_smartbev"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


# Define the Category model


class Category(Base):
    __tablename__ = "categorysensors"
    id = Column(Integer, primary_key=True)
    sensor = Column(String(255))

class SensorsData(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True)
    idDistr = Column(Integer)
    idSensor = Column(Integer)
    value = Column(String(255))


Base.metadata.create_all(bind=engine)

@app.get('/ODB/categories')
def get_categories():
    db = SessionLocal()

    categories = db.query(Category).all()
    category_list = [{'id': category.id, 'sensor': category.sensor} for category in categories]

    db.close()

    return category_list


@app.post('/ODB/sensors/data')
def addDataSensors(sensors: list[dict]):
    db = SessionLocal()

    for sensor in sensors:
        data = SensorsData(
            idDistr=sensor['idDistr'],
            idSensor=sensor['idSensor'],
            value=sensor['value']
        )
        db.add(data)

    db.commit()
    db.close()

    return {"message": "Data inserted successfully."}


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(app, host='0.0.0.0', port=8000)
