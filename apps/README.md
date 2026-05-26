# Waypik Backend - Modular Structure

Welcome to the new modular backend! This structure is designed for high scalability and clear separation of concerns.

## 📁 Project Structure

### 1. `core/` (The Brain)
- **Settings**: Split into `base.py`, `dev.py`, and `prod.py`.
- **WSGI/ASGI**: Entry points for the web server.
- **URLs**: Root routing for the entire API.

### 2. `apps/` (The Features)
Each feature (e.g., `transport`, `users`, `bookings`) follows a standard professional layout:
- **`models/`**: Data definitions.
- **`api/`**: Contains `views/` and `serializers/` for the mobile app endpoints.
- **`services/`**: The "Heart" of the app. All business logic (calculations, complex checks) goes here.
- **`selectors.py`**: Clean, reusable database queries.
- **`tasks.py`**: Background jobs (like sending notifications).

### 3. `common/`
- Contains shared logic used across all apps.
- **`BaseModel`**: Every model in this project inherits from `BaseModel`, giving it a **UUID** and timestamps automatically.

---

## 🛠️ Development Tips
- **Models**: If you add a new model, put it in `apps/<feature>/models/` and expose it in `__init__.py`.
- **Logic**: Never put logic in `views.py`. Create a function in `services/` and call it from the view.
- **Migrations**: Always run `python manage.py makemigrations <app_name>` to keep things clean.
