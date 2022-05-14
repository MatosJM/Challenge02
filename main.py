from fastapi import FastAPI
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import select

app = FastAPI()

Base = declarative_base()
databaseURL = "mysql://guest:relational@relational.fit.cvut.cz:3306/tpcd"
engine = db.create_engine(databaseURL)

metadata = db.MetaData()
connection = engine.connect()

#root
@app.get("/")
async def root():
    return {"message": "Hello World"}

#database
dss_customer = db.Table( 'dss_customer' , metadata, autoload= True, autoload_with=engine)

#metodo getAll

@app.get("/customers")
def get_AllCustomers():
    
    query = db.select([dss_customer])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchmany( 10)

    return ResultSet
@app.get("/customers/{segment}")   
def get_CustomersBySegment(segment: str):
    
    query = db.select([dss_customer]).where([dss_customer].c_mktsegment.in_(segment))
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchmany( 10)

    return ResultSet

