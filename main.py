from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from decimal import Decimal
from bank import Account

app = FastAPI()
accounts_db = {}

class account(BaseModel):
    name: str
    balance: float = 0.0
    
@app.post("/accounts/")
def create_account(data:account):
    
    if data.name in accounts_db:
        raise HTTPException(status_code=400, detail=f"บัญชี '{data.name}' มีอยู่แล้ว")
    
    new_account = Account(
        name = data.name,
        balance = Decimal(str(data.balance))
    )

    accounts_db[data.name] = new_account

    return {
        "status": "success",
        "name" : new_account.name,
        "balance" : str(new_account.balance),
        "history" : new_account.history
        }
    
@app.post("/accounts/{name}/deposit")
def deposit(name: str, amount: float):
    if name not in accounts_db:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{name}'")
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="จำนวนเงินต้องมากกว่า 0")
    
    account = accounts_db[name]
    account.deposit(Decimal(str(amount)))
    
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
def withdraw(name: str, amount: float):
    if name not in accounts_db:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{name}'")
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="จำนวนเงินต้องมากกว่า 0")
    
    account = accounts_db[name]
    

    if amount > account.balance:
        raise HTTPException(status_code=400, detail=f"เงินไม่พอ! มี {account.balance} บาท แต่จะถอน {amount} บาท")
    
    account.withdraw(Decimal(str(amount)))
    
    return {
        "status": "success",
        "message": f"ถอนเงิน {amount} บาท สำเร็จ",
        "account": {
            "name": account.name,
            "balance": str(account.balance),
            "history": account.history
        }
    }    
    
    
@app.post("/accounts/{from_name}/transfer")
def transfer(from_name: str, to_name: str, amount: float):
    # เช็คบัญชีต้นทาง
    if from_name not in accounts_db:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{from_name}'")
    
    # เช็คบัญชีปลายทาง
    if to_name not in accounts_db:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{to_name}'")
    
    # เช็คจำนวนเงิน
    if amount <= 0:
        raise HTTPException(status_code=400, detail="จำนวนเงินต้องมากกว่า 0")
    
    # เช็คโอนตัวเอง
    if from_name == to_name:
        raise HTTPException(status_code=400, detail="ไม่สามารถโอนเข้าบัญชีตัวเองได้")
    
    from_account = accounts_db[from_name]
    to_account = accounts_db[to_name]
    
    # เช็คเงินพอไหม
    if amount > from_account.balance:
        raise HTTPException(status_code=400, detail=f"เงินไม่พอ! มี {from_account.balance} บาท แต่จะโอน {amount} บาท")
    
    # โอนเงิน (ใช้ method transfer จาก bank.py)
    from_account.transfer(to_account, Decimal(str(amount)))
    
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
        },
        "history": from_account.history
    }    
    
    
@app.get("/accounts/{name}")
def get_account(name: str, limit: int = None):
    if name not in accounts_db:
        raise HTTPException(status_code=404, detail=f"ไม่พบบัญชี '{name}'")
    
    account = accounts_db[name]
    
    if limit:
        history = account.history[-limit:]
    else:
        history = account.history
    
    return {
        "name": account.name,
        "balance": str(account.balance),
        "history": history,
        "total_history": len(account.history)
    }    
    
    
    