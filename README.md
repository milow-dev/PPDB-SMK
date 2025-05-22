# Sistem PPDB SMK

Sistem Penerimaan Peserta Didik Baru (PPDB) untuk SMK menggunakan Flask.

## Fitur

- Autentikasi multi-user (Admin & Siswa)
- Formulir pendaftaran online
- Dashboard admin untuk verifikasi pendaftaran
- Manajemen status pendaftaran
- Sistem pembayaran dengan upload bukti
- Notifikasi status pendaftaran

## Teknologi

- Python 3.x
- Flask Framework
- SQLite Database
- Bootstrap 5
- Flask-Login untuk autentikasi
- Flask-SQLAlchemy untuk ORM
- Flask-Migrate untuk migrasi database

## Instalasi

1. Clone repository
```bash
git clone <repository-url>
cd PPDB-SMK
```

2. Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup database
```bash
flask db upgrade
```

5. Jalankan aplikasi
```bash
python run.py
```

## Struktur Project

