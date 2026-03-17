from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import hashlib
import uuid
import json
import datetime

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra nodes
session = cluster.connect('ecommerce')  # Keyspace name

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    return str(uuid.uuid4())

@csrf_exempt
@require_POST
def register_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"message": "Username and password are required"}, status=400)
        if len(password) < 6:
            return JsonResponse({"message": "Password must be at least 6 characters long"}, status=400)

        # Check if user exists
        query = "SELECT username FROM users WHERE username=%s"
        result = session.execute(query, (username,))
        if result.one():
            return JsonResponse({"message": "Username already taken"}, status=400)

        # Insert new user
        password_hash = hash_password(password)
        token = generate_token()
        created_at = datetime.datetime.utcnow()

        insert_query = """
            INSERT INTO users (username, password_hash, token, created_at)
            VALUES (%s, %s, %s, %s)
        """
        session.execute(insert_query, (username, password_hash, token, created_at))

        return JsonResponse({
            "message": "Account created successfully. You can now log in.",
            "success": True,
            "token": token
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"message": f"Error: {str(e)}"}, status=500)

@csrf_exempt
@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"message": "Username and password required"}, status=400)

        # Fetch user
        query = "SELECT username, password_hash, token FROM users WHERE username=%s"
        user_row = session.execute(query, (username,)).one()
        if not user_row:
            return JsonResponse({"message": "Invalid credentials"}, status=400)

        if user_row.password_hash != hash_password(password):
            return JsonResponse({"message": "Invalid credentials"}, status=400)

        # Generate new token
        token = generate_token()
        update_query = "UPDATE users SET token=%s WHERE username=%s"
        session.execute(update_query, (token, username))

        return JsonResponse({
            "message": "Login successful!",
            "username": username,
            "token": token
        }, status=200)

    except Exception as e:
        return JsonResponse({"message": f"Error: {str(e)}"}, status=500)

@csrf_exempt
@require_POST
def logout_view(request):
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Token "):
            token_key = auth_header.split(" ")[1]

            # Remove token from user table
            query = "UPDATE users SET token=NULL WHERE token=%s"
            session.execute(query, (token_key,))

        return JsonResponse({"message": "Logged out successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Something went wrong: {str(e)}"}, status=400)
