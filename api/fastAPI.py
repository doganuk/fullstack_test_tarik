import os
import time
import boto3
from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from boto3.dynamodb.conditions import Key
import json
from random import randint, random
import datetime
from datetime import date, datetime, time, timedelta
from createData import flight_data

app = FastAPI()
handler = Mangum(app)


class PutTaskRequest(BaseModel):
    source: str
    sink: Optional[str] = None
    airline: Optional[str] = None
    departure_dt: Optional[str] = None
    arrival_dt: Optional[str] = None
    number_of_stops: Optional[str] = None
    emissions: Optional[str] = None
    price: Optional[str] = None




@app.get("/")
async def root():
    return {"message": "Hello from fastAPI API!"}

@app.put("/seed")
async def list_flights(put_task_request: PutTaskRequest):
    # with open('generatedData.json', 'r') as myfile:
    #     data=myfile.read()
    # # parse file
    # objects = json.loads(data)

    createdData = flight_data(
    source="London",
    sink="Amsterdam",
    departure_date=date(2024, 10, 3),
    return_date=date(2024, 10, 10),
    )
    for object in createdData:
        item = {
        "id": f"flight_{randint(0, 24000)}",
        "source": object['source'],
        "sink": object['sink'],
        "airline": object['airline'],
        "departure_dt":datetime.strftime(object['departure_dt'],'%d/%m/%Y, %H:%M:%S'), #object['departure_dt'],#object.get('departure_dt'),
        "arrival_dt": datetime.strftime(object['arrival_dt'],'%d/%m/%Y, %H:%M:%S'),#object['arrival_dt'],
        "number_of_stops": object['number_of_stops'],  # Expire after 24 hours.
        "emissions": object['emissions'],
        "price": object['price']
        }          
        table = _get_table()
        table.put_item(Item=item)
    
    return {"success"}
    
@app.get("/list-flight/{source}")
async def list_flights(source: str):
    table = _get_table()
    return table.scan()["Items"]



def _get_table():
    table_name = os.environ.get("TABLE_NAME")
    return boto3.resource("dynamodb").Table(table_name)
