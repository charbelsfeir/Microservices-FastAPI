from time import sleep
from dal import models
from dal.db_helper import engine
from routers import product_controller
from fastapi import FastAPI
import os
import sys
sys.path.append('/app')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product_controller.router)
