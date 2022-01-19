from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dal.models import product_model
from routers.models import models
from sqlalchemy.orm import Session
from hashlib import sha256
from fastapi import HTTPException, status
import os
from fastapi.security import OAuth2PasswordBearer

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://{}:{}@{}/{}".format(
    "root", os.environ["MYSQL_ROOT_PASSWORD"], os.environ["MYSQL_IP_ADDRESS"], os.environ["MYSQL_DATABASE"])
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_product(db: Session, product: models.ProductModel):
    product = product_model.DbProductModel(name=product.name, img_path=product.img_path,
                                           price=product.price, description=product.description, seller_id=product.seller_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def bet(db: Session, product_id: int, price: float, user_id: int):
    product = db.query(product_model.DbProductModel).filter(
        product_model.DbProductModel.id == product_id).first()
    if product:
        if price <= product.price:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="You must bet on higher price than {}".format(
                    product.price),
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            bidding_product = product_model.DbBiddingProductModel(
                product_id=product.id, price=price, buyer_id=user_id)
            db.add(bidding_product)
            db.commit()
            db.refresh(bidding_product)
            return bidding_product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


def submit_question(db: Session, question: models.QuestionModel, user_id: int):
    product = db.query(product_model.DbProductModel).filter(
        product_model.DbProductModel.id == question.product_id).first()
    if product:
        question = product_model.DbQuestionModel(
            content=question.question, product_id=question.product_id, user_id=user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
