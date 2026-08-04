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

## Instalasi & Menjalankan Project

### Prasyarat
- Python 3.10 atau lebih baru
- PostgreSQL 13+ (sudah terinstall dan service berjalan)
- pip / virtualenv
- Git

### 1. Clone Repository
```bash
git clone https://github.com/username/tes-amazink.git
cd tes-amazink
```

### 2. Buat & Aktifkan Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment Variables
Salin file `.env.example` menjadi `.env`, lalu sesuaikan isinya:
```bash
copy .env.example .env      # Windows
cp .env.example .env        # Linux / macOS
```

Isi `.env` minimal berisi:
```env
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/tes_amazink_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
UPLOAD_DIR=uploads
```

### 5. Buat Database di PostgreSQL
```sql
CREATE DATABASE tes_amazink_db;
```

### 6. Jalankan Migrasi Database (Alembic)
```bash
# Inisialisasi migrasi (jika belum ada folder alembic/versions)
alembic revision --autogenerate -m "init tables"

# Terapkan migrasi ke database
alembic upgrade head
```

### 7. Buat Folder Upload (jika belum tersedia)
```bash
mkdir uploads
```

### 8. Jalankan Aplikasi
```bash
uvicorn app.main:app --reload
```

Aplikasi akan berjalan di:

### 9. Akses Dokumentasi API
FastAPI otomatis menyediakan dokumentasi interaktif:
- Swagger UI: `http://127.0.0.1:8000/docs`


## Akun Demo

Setelah menjalankan script seeder, beberapa akun demo berikut akan otomatis tersedia untuk keperluan testing:

### Menjalankan Seeder
```bash
python -m app.seed
# atau sesuaikan path sesuai lokasi file seeder kamu, misal:
# python app/db/seed.py
```

### Daftar Akun Demo

| Role         | Email               | Password      | Keterangan                                  |
|--------------|----------------------|---------------|----------------------------------------------|
| PM IT        | pm@example.com        | password123   | Project Manager IT — akses penuh manajemen tiket |
| Staff IT     | staff@example.com     | password123   | Staff IT — menangani & memproses tiket        |
| User         | user@example.com      | password123   | Regular User — membuat & memantau tiket       |