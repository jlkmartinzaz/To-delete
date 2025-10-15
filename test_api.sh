#!/bin/bash

BASE_URL="http://localhost:5000"

# ----------------------------
# Registrar usuarios
# ----------------------------
echo "=== Registrando usuarios ==="
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
echo
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"user123"}'
echo -e "\n"

# ----------------------------
# Login usuarios
# ----------------------------
echo "=== Login de admin ==="
ADMIN_LOGIN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}')

ADMIN_ACCESS_TOKEN=$(echo $ADMIN_LOGIN | jq -r '.access_token')
ADMIN_REFRESH_TOKEN=$(echo $ADMIN_LOGIN | jq -r '.refresh_token')
echo "Access token: $ADMIN_ACCESS_TOKEN"
echo "Refresh token: $ADMIN_REFRESH_TOKEN"
echo -e "\n"

echo "=== Login de user ==="
USER_LOGIN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"user123"}')

USER_ACCESS_TOKEN=$(echo $USER_LOGIN | jq -r '.access_token')
USER_REFRESH_TOKEN=$(echo $USER_LOGIN | jq -r '.refresh_token')
echo "Access token: $USER_ACCESS_TOKEN"
echo "Refresh token: $USER_REFRESH_TOKEN"
echo -e "\n"

# ----------------------------
# Refresh token
# ----------------------------
echo "=== Refresh token de admin ==="
ADMIN_NEW_TOKEN=$(curl -s -X POST "$BASE_URL/auth/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_REFRESH_TOKEN")

echo $ADMIN_NEW_TOKEN | jq
echo -e "\n"

# ----------------------------
# CRUD de gatos
# ----------------------------
echo "=== Crear un gato (admin) ==="
curl -s -X POST "$BASE_URL/cats/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" \
  -d '{"name":"Michi","breed":"Siamese","age":3,"adopted":false,"color":"Brown","weight":4.2}' | jq
echo -e "\n"

echo "=== Listar gatos (user) ==="
curl -s -X GET "$BASE_URL/cats/" \
  -H "Authorization: Bearer $USER_ACCESS_TOKEN" | jq
echo -e "\n"

echo "=== Actualizar gato (admin) ==="
curl -s -X PUT "$BASE_URL/cats/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" \
  -d '{"age":4,"adopted":true}' | jq
echo -e "\n"

echo "=== Eliminar gato (admin) ==="
curl -s -X DELETE "$BASE_URL/cats/1" \
  -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" | jq
echo -e "\n"
