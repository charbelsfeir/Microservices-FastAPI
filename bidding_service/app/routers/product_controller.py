import sys
import os
import pathlib
import shutil
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status
from starlette.responses import JSONResponse
from routers.models.models import ProductModel, QuestionModel
from datetime import datetime
from dal.db_helper import SessionLocal
from sqlalchemy.orm import Session
from dal import db_helper
import requests

router = APIRouter()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
authentication_url = "{}/{}".format(
    os.environ["USER_SERVICE_API"], "api/profile")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/api/product/create', tags=["Product"])
def post_product(product: ProductModel, request: Request, db: Session = Depends(get_db)):
    # print(request.headers.get("Authorization"))
    try:
        token = request.headers.get("Authorization")
    except:
        raise credentials_exception
    result = requests.get(authentication_url,
                          headers={'Content-Type': 'application/json',
                                   'Authorization': '{}'.format(token)})
    print(result.status_code)
    if result.status_code == 401:
        raise credentials_exception
    elif result.status_code == 200:
        if result.json()["role"]["name"] == "seller":
            product.seller_id = result.json()["id"]
            return db_helper.create_product(db, product)
        else:
            return {"response": "You are not elligible to post products"}


@router.get('/api/product/bet', tags=["Product"])
def bet(product_id: int, price: float, request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("Authorization")
    except:
        raise credentials_exception
    result = requests.get(authentication_url,
                          headers={'Content-Type': 'application/json',
                                   'Authorization': '{}'.format(token)})
    print(result.status_code)
    if result.status_code == 401:
        raise credentials_exception
    elif result.status_code == 200:
        if result.json()["role"]["name"] == "buyer":
            return db_helper.bet(db, product_id, price, result.json()["id"])
        else:
            return {"response": "You are not elligible to bet on products"}


@router.post('/api/product/q&a', tags=["Product"])
def ask_question(question: QuestionModel, request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("Authorization")
    except:
        raise credentials_exception
    result = requests.get(authentication_url,
                          headers={'Content-Type': 'application/json',
                                   'Authorization': '{}'.format(token)})
    print(result.status_code)
    if result.status_code == 401:
        raise credentials_exception
    elif result.status_code == 200:
        question = db_helper.submit_question(db, question, result.json()["id"])
        return question
# db_user = db_helper.get_user_by_email(db, email=user.email)
# if db_user:
#     raise HTTPException(status_code=400, detail="Email already registered")
# return db_helper.create_user(db=db, user=user)
# result = "Hello and welcome to microservices course"
# return result
