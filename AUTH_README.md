# Authentication System Documentation

This project implements a complete OAuth2 authentication flow with password hashing and JWT tokens using FastAPI, SQLModel, and Alembic.

## Features

- **User Registration**: Create new user accounts with email and password
- **User Login**: Authenticate users with email/password and receive JWT tokens
- **Password Hashing**: Secure password storage using bcrypt
- **JWT Tokens**: Stateless authentication with configurable expiration
- **Protected Routes**: Easy-to-use dependency injection for route protection
- **Database Integration**: SQLModel with Alembic migrations

## API Endpoints

### Authentication Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user information
- `GET /auth/users/{user_id}` - Get user by ID (protected)

### Example Endpoints

- `GET /protected` - Example protected route

## Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Access Protected Route

```bash
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. Get Current User Info

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Database Setup

1. Run the Alembic migration to create the user table:
   ```bash
   alembic upgrade head
   ```

2. The database will be created automatically when you start the application.

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string (default: `sqlite:///./recurly.db`)
- `SECRET_KEY`: JWT secret key (change in production!)

### Security Settings

- **Password Hashing**: Uses bcrypt with automatic salt generation
- **JWT Expiration**: 30 minutes (configurable in `auth.py`)
- **Algorithm**: HS256
- **Token Type**: Bearer

## Project Structure

```
recurly/
├── models.py          # SQLModel user models
├── auth.py           # Authentication utilities
├── database.py       # Database configuration
├── schemas.py        # Pydantic schemas
├── routes.py         # Authentication routes
└── __init__.py       # Package exports

alembic/
├── versions/         # Database migrations
└── env.py           # Alembic configuration

main.py              # FastAPI application
```

## Security Considerations

1. **Change the SECRET_KEY** in production
2. **Use HTTPS** in production
3. **Configure CORS** properly for your frontend
4. **Use environment variables** for sensitive configuration
5. **Consider rate limiting** for login endpoints
6. **Implement email verification** for user registration

## Dependencies

- `fastapi[standard]` - Web framework
- `sqlmodel` - Database ORM
- `alembic` - Database migrations
- `python-jose[cryptography]` - JWT token handling
- `passlib[bcrypt]` - Password hashing
- `python-multipart` - Form data handling
- `email-validator` - Email validation

## Running the Application

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the application:
   ```bash
   uv run uvicorn main:app --reload
   ```

3. Visit `http://localhost:8000/docs` for interactive API documentation.
