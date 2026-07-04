cat > README.md << 'EOF'
# Python Banking System 🏦

ระบบธนาคารง่ายๆ เขียนด้วย Python

## Features
- ฝาก/ถอน/โอนเงิน
- Transaction history
- บันทึกข้อมูลลง JSON
- Rollback เมื่อเกิด error
- REST API ด้วย FastAPI

## การใช้งาน
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```
EOF