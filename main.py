from fastapi import FastAPI, HTTPException, Query,Depends
from pydantic import BaseModel
from decimal import Decimal
from models import AccountModel, TransactionModel
from db import get_db, Base, engine
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()
Base.metadata.create_all(bind=engine)

class account(BaseModel):
    name: str
    balance: float = 0.0
    
class TransferRequest(BaseModel):
    amount: Decimal    
    
@app.post("/accounts/")
def create_account(data:account, db: Session = Depends(get_db)):
    
    accounts = db.query(AccountModel).filter(AccountModel.name == data.name).first()
    
    if accounts:
        raise HTTPException(status_code=400, detail=f"บัญชี '{data.name}' มีอยู่แล้ว")
    
    new_account = AccountModel(
        name = data.name,
        balance = Decimal(str(data.balance))
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {
        "status": "success",
        "name" : new_account.name,
        "balance" : str(new_account.balance),
        "history" : new_account.history
        }
    
@app.post("/accounts/{name}/deposit")
def deposit(name: str, data: TransferRequest, db: Session =Depends(get_db)):
    
    account = db.query(AccountModel).filter(AccountModel.name == name).first()
    
    if not account:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{name}'")
    
    amount = data.amount
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="จำนวนเงินต้องมากกว่า 0")
    
    account.balance += amount
    tx =TransactionModel(
        account_id = account.id,
        message = f"ฝากเงิน {amount} บาท",
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(tx)
    db.commit()
    db.refresh(account)
   
    return {
        "status": "success",
        "message": f"ฝากเงิน {amount} บาท สำเร็จ",
        "account": {
            "name": account.name,
            "balance": str(account.balance),
            "history": account.history
        }
    }

@app.post("/accounts/{name}/withdraw")
def withdraw(name: str, data: TransferRequest, db: Session = Depends(get_db)):
    
    account = db.query(AccountModel).filter(AccountModel.name == name).first()
    
    if not account:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{name}'")
    
    amount = data.amount
    
    if amount > account.balance:
        raise HTTPException(status_code=400, detail=f"เงินไม่พอ!")
    
    
    account.balance -= amount
    
    
    tx = TransactionModel(
        account_id = account.id,
        message = f"ถอนเงิน {amount} บาท",
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(tx)
    db.commit()
    db.refresh(account)
    
    return {
        "status": "success",
        "balance": str(account.balance)
    }

@app.post("/accounts/{from_name}/transfer")
def transfer(from_name: str,to_name: str, data: TransferRequest,db: Session = Depends(get_db)):

    from_account = db.query(AccountModel).filter(AccountModel.name == from_name).first()

    if not from_account:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{from_name}'")

    
    to_account = db.query(AccountModel).filter(AccountModel.name == to_name).first()

    if not to_account:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{to_name}'")

   
    if from_name == to_name:
        raise HTTPException(status_code=400, detail="ไม่สามารถโอนเข้าบัญชีตัวเองได้")

    amount = data.amount

    if amount <= 0:
        raise HTTPException(status_code=400, detail="จำนวนเงินต้องมากกว่า 0")

    if amount > from_account.balance:
        raise HTTPException(
            status_code=400,
            detail=f"เงินไม่พอ! มี {from_account.balance} บาท แต่จะโอน {amount} บาท"
        )

    
    from_account.balance -= amount
    to_account.balance += amount

    
    db.add(TransactionModel(
        account_id=from_account.id,
        message=f"โอนเงินไป {to_name} {amount}",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    
    db.add(TransactionModel(
        account_id=to_account.id,
        message=f"รับเงินจาก {from_name} {amount}",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    
    db.commit()

    return {
        "status": "success",
        "message": f"โอนเงิน {amount} บาท จาก {from_name} ไป {to_name} สำเร็จ",
        "from": {
            "name": from_account.name,
            "balance": str(from_account.balance)
        },
        "to": {
            "name": to_account.name,
            "balance": str(to_account.balance)
        }
    }
    
@app.get("/accounts/{name}")
def get_account(name: str, limit: int | None = Query(default=None, ge=1), db: Session = Depends(get_db)):
    
    account = db.query(AccountModel).filter(AccountModel.name == name).first()
    
    if not account:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{name}'")
    
    transactions = db.query(TransactionModel).filter(
        TransactionModel.account_id == account.id
    ).all()
    
    history = [t.message for t in transactions]
    
    if limit:
        history = history[-limit:]
    
    return {
        "name": account.name,
        "balance": str(account.balance),
        "history": history,
        "total_history": len(transactions)
    }
    
    
    