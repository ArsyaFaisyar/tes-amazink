# Ticketing System RESTful API

RESTful API backend untuk sistem pelaporan Bug dan Feature Request. Dibuat sebagai solusi Technical Test Backend Developer - PT Wahana Solusi Sistem Indonesia.

Aplikasi ini dibangun menggunakan FastAPI, PostgreSQL, SQLAlchemy ORM v2.0, Pydantic v2, dan JWT Authentication dengan pendekatan Clean Architecture / Modular Structure yang scalable dan maintainable.

---

## Tech Stack & Dependencies

- Framework: FastAPI (Python 3.10+)
- Database & ORM: PostgreSQL + SQLAlchemy v2.0
- Database Migration: Alembic
- Authentication: JWT (PyJWT / Passlib dengan Bcrypt)
- Validation & Schemas: Pydantic v2 / Pydantic-Settings
- Server: Uvicorn

---

## Struktur Folder Project

```text
D:\tes-amazink/
│
├── alembic/                    # Skrip & histori migrasi database
├── uploads/                    # Folder penyimpanan lampiran tiket (attachments)
├── app/
│   ├── core/                   # Konfigurasi utama, database session, security/JWT
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── models/                 # SQLAlchemy ORM Database Models
│   │   └── all_models.py
│   │
│   ├── schemas/                # Pydantic v2 Schemas / DTOs
│   │   └── all_schemas.py
│   │
│   ├── services/               # Logic bisnis, State Machine, Audit Log automatization
│   │   ├── auth_service.py
│   │   ├── ticket_service.py
│   │   └── comment_service.py
│   │
│   ├── routers/                # HTTP Endpoints & Controllers
│   │   ├── auth_router.py
│   │   ├── ticket_router.py
│   │   ├── comment_router.py
│   │   ├── attachment_router.py
│   │   ├── dashboard_router.py
│   │   └── system_router.py
│   │
│   └── main.py                 # Entry point aplikasi FastAPI
│
├── .env                        # Environment variables
├── .gitignore
├── alembic.ini                 # Konfigurasi Alembic
├── README.md                   # Dokumentasi Utama Project
└── requirements.txt            # Daftar dependencies project