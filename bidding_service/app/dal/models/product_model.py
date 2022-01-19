from itertools import product
from operator import index
from tokenize import Floatnumber
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from dal.models import Base


class DbBiddingProductModel(Base):
    __tablename__ = "bidding_prod"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"))
    products = relationship(
        "DbProductModel", back_populates="bidding_products")
    buyer_id = Column(Integer)


class DbQuestionModel(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255))
    product_id = Column(Integer, ForeignKey("product.id"))
    products = relationship(
        "DbProductModel", back_populates="questions")
    user_id = Column(Integer)


class DbProductModel(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    img_path = Column(String(255))
    price = Column(Float)
    description = Column(String(255))
    bidding_products = relationship(
        "DbBiddingProductModel", back_populates="products")
    questions = relationship("DbQuestionModel", back_populates="products")
    seller_id = Column(Integer)
