# Authentication Plan: JWT Tokens

## Overview
Implement JWT (JSON Web Token) authentication between the NextJS frontend and FastAPI backend.

---

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   NextJS FE     │         │   FastAPI BE    │
│                 │         │                 │
│  Login Form     │──POST──▶│  /auth/login    │
│                 │◀─JWT────│                 │
│                 │         │                 │
│  Store token    │         │                 │
│  (httpOnly      │         │                 │
│   cookie or     │         │                 │
│   memory)       │         │                 │
│                 │         │                 │
│  API Request    │──JWT───▶│  Protected      │
│  + Auth Header  │◀─data───│  Endpoints      │
└─────────────────┘         └─────────────────┘
```

---

## Dependencies to Add

```
# requirements.txt
python-jose[cryptography]>=3.3.0  # JWT encoding/decoding
passlib[bcrypt]>=1.7.4            # Password hashing
python-multipart>=0.0.6           # Form data parsing
```

---

## Implementation Steps

### Phase 1: User Model & Database

1. Create User model with fields:
   - id (primary key)
   - email (unique, indexed)
   - hashed_password
   - is_active (default: True)
   - created_at
   - updated_at

2. Create migration for users table

3. Create schemas:
   - UserCreate (email, password)
   - UserRead (id, email, is_active, created_at)
   - UserLogin (email, password)

### Phase 2: Password Hashing

1. Create `app/auth/security.py`:
   - `hash_password(password: str) -> str`
   - `verify_password(plain: str, hashed: str) -> bool`

2. Use bcrypt with passlib for secure hashing

### Phase 3: JWT Token Management

1. Add config settings:
   - `SECRET_KEY` - Random secret for signing tokens
   - `ALGORITHM` - HS256
   - `ACCESS_TOKEN_EXPIRE_MINUTES` - 30

2. Create `app/auth/jwt.py`:
   - `create_access_token(data: dict, expires_delta: timedelta) -> str`
   - `decode_token(token: str) -> dict`

3. Token payload structure:
   ```json
   {
     "sub": "user_id",
     "email": "user@example.com",
     "exp": 1234567890
   }
   ```

### Phase 4: Auth Endpoints

1. Create `app/routers/auth.py`:

   **POST /auth/register**
   - Input: email, password
   - Validate email format
   - Check email not already registered
   - Hash password
   - Create user
   - Return UserRead

   **POST /auth/login**
   - Input: email, password (OAuth2PasswordRequestForm)
   - Verify credentials
   - Generate JWT token
   - Return: `{ "access_token": "...", "token_type": "bearer" }`

   **GET /auth/me**
   - Requires authentication
   - Return current user info

### Phase 5: Protected Routes

1. Create `app/auth/dependencies.py`:
   - `get_current_user(token: str = Depends(oauth2_scheme)) -> User`
   - Decode token
   - Fetch user from database
   - Raise 401 if invalid

2. Create OAuth2 scheme:
   ```python
   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
   ```

3. Protect pizzeria endpoints:
   ```python
   @app.post("/pizzerias")
   async def create_pizzeria(
       pizzeria: PizzeriaCreate,
       current_user: User = Depends(get_current_user),
       session: AsyncSession = Depends(get_session),
   ):
   ```

### Phase 6: Frontend Integration

1. **Login flow (NextJS):**
   ```typescript
   const response = await fetch('/api/auth/login', {
     method: 'POST',
     body: new URLSearchParams({ username: email, password }),
   });
   const { access_token } = await response.json();
   ```

2. **Token storage options:**

   **Option A: Memory + Refresh Token (Recommended)**
   - Store access token in memory (React state/context)
   - Store refresh token in httpOnly cookie
   - More secure against XSS

   **Option B: httpOnly Cookie**
   - Backend sets httpOnly cookie with token
   - Automatically sent with requests
   - Need CSRF protection

   **Option C: localStorage (Not recommended)**
   - Vulnerable to XSS attacks
   - Easy to implement but less secure

3. **API requests with token:**
   ```typescript
   fetch('/api/pizzerias', {
     headers: {
       'Authorization': `Bearer ${accessToken}`,
     },
   });
   ```

---

## Project Structure (Target)

```
backend/
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py  # get_current_user
│   │   ├── jwt.py           # Token creation/validation
│   │   └── security.py      # Password hashing
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pizzeria.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── pizzerias.py
│   ├── config.py
│   ├── database.py
│   └── main.py
```

---

## Environment Variables

```env
SECRET_KEY=your-super-secret-key-generate-with-openssl-rand-hex-32
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate secret key:
```bash
openssl rand -hex 32
```

---

## Security Considerations

1. **Password Requirements:** Minimum 8 characters
2. **Token Security:** Short expiration (30 min), use refresh tokens
3. **Rate Limiting:** Limit login attempts
4. **CORS:** Configure allowed origins, no wildcards in production
5. **HTTPS:** Always use in production

---

## Testing Plan

1. **Unit tests:**
   - Password hashing/verification
   - Token creation/decoding
   - Token expiration

2. **Integration tests:**
   - Register new user
   - Login with valid/invalid credentials
   - Access protected routes with/without token
   - Expired token handling

---

## Migration Script

```python
# alembic/versions/003_add_users_table.py

def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_email", "user", ["email"], unique=True)
```

---

## Optional Enhancements

1. **Refresh Tokens** - Longer-lived token for session management
2. **Email Verification** - Verify email before allowing login
3. **Password Reset** - Forgot password flow
4. **OAuth2 Providers** - Google/GitHub login
5. **Role-Based Access Control** - Admin vs user permissions
