# Register
curl -X POST http://localhost:8000/auth/register \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"test123"}'

# Login (returns tokens)
curl -X POST http://localhost:8000/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"test123"}'

# Use token to create pizzeria
curl -X POST http://localhost:8000/pizzerias \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your-access-token>" \
-d '{"name":"Test Pizza","address":"Berlin"}'