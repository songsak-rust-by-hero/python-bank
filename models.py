from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class AccountModel(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Numeric(12, 2))

    history = relationship("TransactionModel", back_populates="account")


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    message = Column(String)
    timestamp = Column(String)

    account = relationship("AccountModel", back_populates="history")