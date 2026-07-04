from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
import time
import json

@dataclass
class Account:
    name: str
    balance: Decimal = Decimal('0.00')
    history: list[str] = field(default_factory=list)
    
    def deposit(self,amount:Decimal):
        if amount <= 0 :
            return print("เงินฝากน้อยกว่า0ฝากไม่ได้")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.balance += amount
        print(f"ฝากเงินสำเร็จ {amount} ยอดคงเหลือ {self.balance} บาท")
        
        self.history.append(f"[{current_time}] ฝากเงิน{amount} บาท")
        
    def withdraw(self,amount:Decimal):
        if amount <= 0:
            return print("ยอดเงินถอนต้องมากกว่า0")
         
        if amount > self.balance:
            return print(f"เงินไม่พอถอน มีอยู่{self.balance} จะถอน{amount}")
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        self.balance -= amount
        print(f"ถอนเงินในบันชี {amount} บาท คงเหลือในบันชี {self.balance} บาท")    
        
        self.history.append(f"[{current_time}] ถอนเงิน{amount} บาท")
        
        
    def  transfer(self, target_account:'Account', amount:Decimal):
        if amount <=0:
          return print("เกิดข้อผิดพลาดเงินโอนน้อยกว่า0") 
      
        if amount > self.balance:
            return print(f"ไม่สามารถโอนเงินได้ จำนวนเงินบันชีน้อยกว่ายอดโอน {self.name} มีแค่ {self.balance} บาท")           
           
        if self == target_account:
            return print(f"โอนบันชีตัวเองไม่ได้")
        
        old_self_balance = self.balance
        old_target_balance = target_account.balance
        
        try:
           self.balance -= amount
           target_account.balance += amount
           
           current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
           print(f"โอนเงิน{amount} บาท จาก {self.name} ไปยัง {target_account.name} สำเร็จ ")
           self.history.append(f"[{current_time}] โอนเงินไปยัง{target_account.name} จำนวนเงิน{amount} บาท")
        
        except Exception as e:
            self.balance = old_self_balance
            target_account.balance = old_target_balance
            print(f" ระบบขัดข้องกะทันหัน: {e} | ทำการคืนเงิน (Rollback) เรียบร้อย")
            
        
    def print_recent_statement(self,n:int |None = None):
        
        if not self.history:
            print(f"ยังไม่มีประวัติทำรายการ")
            return
        
        if n is None:
            recent_history = self.history
            print(f"\n--- 📄 ประวัติรายการทั้งหมดของ {self.name} (มี {len(self.history)} รายการ) ---")

        else:    
            recent_history = self.history[-n:]
            print(f"\n--- 📄 ประวัติ {n} รายการล่าสุดของ {self.name} ---")
        
        for record in recent_history:
            print(record)

        
    def save_to_json(self,filename:str):
        account_data = {
            "name": self.name,
            "balance": str(self.balance),
            "history": self.history
        }
        with open(filename, "w", encoding="utf-8",)as f:
            json.dump(account_data, f, ensure_ascii=False, indent=4)
        
        print(f"บันทึกลงไฟล์{filename} บันชีชื่อ{self.name} สำเร็จ" )
        
        
    @classmethod
    def load_from_json(cls, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            account_data = json.load(f)
            
        name = account_data["name"]
        balance = Decimal(account_data["balance"])
        history = account_data["history"]
        
        new_account = cls(name=name, balance=balance)
        new_account.history = history
        return new_account    
        
        
user1 = Account('ก้อง') 
user2 = Account('นิ้ง')

user1.deposit(Decimal('200.00'))
time.sleep(1)
user2.deposit(Decimal('500.00'))
time.sleep(2)
user1.withdraw(Decimal('100.00'))
time.sleep(3)
user1.deposit(Decimal('500.00'))
time.sleep(2)
user1.transfer(user2,Decimal('300.00'))          
time.sleep(5)

user1.print_recent_statement()
user1.print_recent_statement(3)

user1.save_to_json(f"{user1.name}.json")

print("--- จบรอบแรก ปิดโปรแกรมจำลอง --- \n")

# 2. รอบสอง: ชุบชีวิตตัวแปรเดิมกลับมาทำงานต่อจากไฟล์ JSON
user1 = Account.load_from_json(f"{user1.name}.json")
user1.print_recent_statement()