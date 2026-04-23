# Waypik Transport Project - Backend 🚀

Welcome to the backend of **Waypik**, a state-of-the-art transport management system built with Django and PostgreSQL.

## 🛠️ Technology Stack

- **Framework**: [Django 5.2](https://www.djangoproject.com/)
- **API**: [Django REST Framework](https://www.django-rest-framework.org/)
- **Database**: [PostgreSQL (Neon Cloud)](https://neon.tech/)
- **Auth**: JWT (SimpleJWT) + dj-rest-auth + allauth
- **Deployment**: [Render](https://render.com/)

## 📂 Project Structure

```text
├── config/             # Project settings and core URLs
├── users/              # Custom User model and Auth logic
├── transport/          # Transport/Vehicle management (Coming soon)
├── bookings/           # Booking and scheduling (Coming soon)
├── docs/               # Detailed API and Setup documentation
├── static/             # Static files
└── manage.py           # Django management script
```

## 📖 Documentation

Detailed documentation for setup and API usage can be found in the `docs/` directory:

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Authentication Setup](docs/AUTHENTICATION_SETUP.md)
- [Authentication Flows](docs/AUTHENTICATION_FLOWS.md)

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL (or Neon Connection String)

### Setup
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd waypik-backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root and add your configuration (see `docs/AUTHENTICATION_SETUP.md` for details).

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## 🔒 Security
- **JWT Authentication**: Secure token-based access.
- **Throttling**: Rate limiting on sensitive endpoints (Login/Register).
- **Environment Safety**: Sensitive keys managed via `.env`.

---
*Created with ❤️ for the Waypik Transport Project.*
