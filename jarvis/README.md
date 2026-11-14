# GD COLLECTION JARVIS AI

Phone-first starter project for a private GD COLLECTION business assistant.

## Files in this starter
- `app.py`: Flask backend with session login, health check, lead CRUD starter, and reference product list.
- `static/index.html`: initial dark-blue JARVIS-style login/status screen.
- `requirements.txt`: Python dependencies.
- `Procfile`: Gunicorn web process.

## Reference catalog
The six prices in the starter are remembered reference prices only. Confirm current prices before quoting customers.

## Required server environment variables
- `APP_PASSWORD`: strong private admin password.
- `SECRET_KEY`: long random secret used to sign sessions.
- `DATABASE_PATH`: persistent database file path on a host with persistent storage.
- `COOKIE_SECURE=1`: keep secure cookies enabled on HTTPS.

Never put secrets in this public GitHub repository. Set them only in the hosting provider's private environment settings.

## Important deployment warning
This is an early starter, not a finished production system. Before entering real customer data, add robust user management, CSRF protection, backups, database migrations, rate limiting, and test the hosting provider's persistent-storage behavior. Do not deploy publicly without HTTPS and the required secrets.

## Current status
Source files have been committed to GitHub. Hosting, live database persistence, AI model connection, Android APK, and Shopee integration are NOT configured. The browser screen is a starter interface, not a finished assistant.
