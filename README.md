# 🏦 Banking System API

REST API สำหรับระบบธนาคารพื้นฐาน ด้วย FastAPI + SQLAlchemy

## 🚀 Features

- สร้างบัญชีธนาคาร
- ฝาก/ถอน/โอนเงิน
- ประวัติการทำรายการ
- Swagger UI Docs
- Unit Test ครอบคลุม 6 กรณี

## 🛠️ Tech Stack

- Python 3.8+
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pytest

## ⚡ Quick Start

```bash
# Clone
git clone <https://github.com/songsak-rust-by-hero/python-bank.git>
cd banking-api

# Install
pip install -r requirements.txt

# Run
uvicorn main:app --reload

# Docs: http://localhost:8000/docs
```

## 📁 Project Structure

```
.
├── main.py          # API endpoints
├── models.py        # Database models (Account, Transaction)
├── db.py           # Database connection
├── test_main.py    # Unit tests (6 tests passing)
├── requirements.txt
├── Procfile        # For deployment
└── .gitignore
```

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/accounts/` | สร้างบัญชี |
| POST | `/accounts/{name}/deposit` | ฝากเงิน |
| POST | `/accounts/{name}/withdraw` | ถอนเงิน |
| POST | `/accounts/{from}/transfer?to_name={to}` | โอนเงิน |
| GET | `/accounts/{name}` | ประวัติรายการ |

## 🧪 Testing

```bash
pytest -v
```

**ผลลัพธ์:** 6 tests passed ✅

## 🚀 Deployment

รองรับบน:
- Railway
- Render (via Procfile)

[Railway Server](https://python-bank-production.up.railway.app/docs)

## 👨‍💻 Developer

**Phet**  
[GitHub](https://github.com/songsak-rust-by-hero)
