```markdown
# Social Media API - Complete Documentation

## 📌 Project Overview
This project is a Social Media API built using Django and Django REST Framework (DRF). The API provides features like:

- JWT authentication
- User profiles
- Post creation and commenting
- Follow system
- Interactive API documentation

## 🚀 Quick Start
### 1. Clone repository
```bash
git clone https://github.com/yourusername/Social_Media_API.git
cd Social_Media_API
```

### 2. Set up environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
nano .env  # Edit variables
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser
```bash
python manage.py createsuperuser
```

### 7. Start server
```bash
python manage.py runserver
```
Access API at: [http://localhost:8000/api/](http://localhost:8000/api/)

## 📂 Project Structure
```bash
Social_Media_API/
├── Social_Media_API/          # Core settings
│   ├── settings.py            # Project configuration
│   ├── urls.py                # Main URL routing
│   └── asgi.py/wsgi.py        # ASGI/WSGI config
├── users/                     # Custom user app
│   ├── models.py              # Custom User model
│   └── authentication/        # JWT logic
├── social/                    # Posts/comments
│   ├── models.py              # Post, Comment models
│   └── serializers.py         # DRF serializers
├── templates/                 # API docs
│   └── index.html             # Interactive docs
├── static/                    # Static files
├── db.sqlite3                 # Dev database
└── manage.py                  # CLI utility
```

## 🔐 Authentication
### JWT Endpoints
| Endpoint                      | Method | Description                |
| ----------------------------- | ------ | -------------------------- |
| `/api/auth/register/`         | POST   | User registration          |
| `/api/auth/login/`            | POST   | Get JWT tokens             |
| `/api/auth/logout/`           | POST   | Invalidate refresh token   |
| `/api/token/refresh/`         | POST   | Refresh access token       |

### Example Request (Login):
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass"}'
```

## 📱 Social Features
### Post Management

```python
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

| Endpoint                     | Method | Description             |
| ---------------------------- | ------ | ----------------------- |
| `/api/posts/create/`         | POST   | Create a new post       |
| `/api/posts/`                | GET    | List all posts          |
| `/api/posts/<pk>/`           | DELETE | Delete post by ID       |

## 🛠 Development Tools
### Management Commands
```bash
python manage.py makemigrations  # Create migrations
python manage.py shell           # Django shell
python manage.py test            # Run tests
```

### Database
- Development: SQLite (db.sqlite3)
- Production: PostgreSQL (recommended)

## ⚙️ Configuration
### settings.py Highlights
```python
AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

## 📦 Dependencies
### Core Requirements
```bash
Django==5.2
djangorestframework==3.16.0
djangorestframework-simplejwt==5.5.0
Pillow==10.3.0  # For image uploads
psycopg2-binary==2.9.6  # PostgreSQL
```

## 🌐 API Documentation
Access interactive docs at: [http://localhost:8000](http://localhost:8000)

## 🚀 Deployment
### Production Checklist
- Set `DEBUG=False` in `.env`
- Configure PostgreSQL
- Set up Gunicorn/Nginx
- Secure with HTTPS

### Sample Gunicorn command
```bash
gunicorn Social_Media_API.wsgi:application --bind 0.0.0.0:8000
```

## 📜 License
MIT License - See LICENSE.md for details.

---

## Social Media API Summary
This is a Social Media API built using Django and Django REST Framework (DRF). The API allows users to register, log in with JWT tokens, create posts, comment on them, like/unlike posts, and follow/unfollow other users. The project includes:

- JWT Authentication for secure access.
- Post management for creating and deleting posts.
- Commenting on posts.
- Likes and Follows systems for user interaction.
- Interactive API Documentation for easy exploration of the API endpoints.

### Features
- **JWT Authentication**: Secure user login and registration with tokens.
- **Post Management**: Users can create, list, and delete posts.
- **Commenting**: Ability to comment on posts.
- **Likes**: Like/unlike posts functionality.
- **Following**: Follow/unfollow other users.
- **Mobile-Friendly UI**: The design ensures the app is responsive.
```
