# Placement Portal Application

A full-stack placement management portal for administrators, companies, and students. The backend uses Flask, SQLite, Redis, and Celery. The frontend uses Vue 3 and Vite.

## Local development guide

### Prerequisites

Install:

- Python 3.10+
- Node.js 20.19+ or 22.12+
- npm
- Redis
- Git

### Clone the repository

```bash
git clone <repository-url>
cd Placement-Portal-Application
```

### Configure backend environment variables

Create `backend/.env`:

```env
SECRET_KEY=replace-with-a-long-random-secret
SECURITY_PASSWORD_SALT=replace-with-another-long-random-secret
Admin=replace-with-the-initial-admin-password

REDIS_URL=redis://localhost:6379/0

MAIL_SERVER=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your-mailtrap-username
MAIL_PASSWORD=your-mailtrap-password
```

Required variables:

- `SECRET_KEY`
- `SECURITY_PASSWORD_SALT`
- `Admin`

Optional variables:

- `REDIS_URL`, default: `redis://localhost:6379/0`
- `MAIL_SERVER`, default: `smtp.mailtrap.io`
- `MAIL_PORT`, default: `2525`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`

Do not commit `.env` files or real credentials.

### Set up the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Start Redis

Run Redis in a separate terminal:

```bash
redis-server
```

### Start the Flask backend

From the `backend` directory:

```bash
python main.py
```

The API runs at:

```text
http://127.0.0.1:3000
```

The SQLite database is stored at:

```text
backend/db_directory/testdb.sqlite3
```

The database, roles, and initial administrator account are initialized when the backend starts.

### Start Celery

Celery is required for scheduled placement-drive reminder emails. Keep Redis and Flask running, then open separate terminals.

From the `backend` directory, activate the virtual environment and run:

```bash
celery -A celery_app.celery worker --loglevel=info
```

In another terminal, run:

```bash
celery -A celery_app.celery beat --loglevel=info
```

### Set up and run the frontend

From the repository root:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, usually:

```text
http://localhost:5173
```

The frontend sends API requests to:

```text
http://localhost:3000
```

No frontend environment variables are required.

### Build the frontend

From the `frontend` directory:

```bash
npm run build
```

The production files are generated in:

```text
frontend/dist/
```

Preview the production build locally:

```bash
npm run preview
```

The Flask backend and Redis must continue running separately.

## Project structure

```text
backend/
  main.py
  celery_app.py
  application/
  db_directory/
  uploads/
  requirements.txt

frontend/
  src/
  public/
  package.json
  vite.config.js
```
