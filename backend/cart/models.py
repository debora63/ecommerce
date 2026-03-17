from cassandra.cluster import Cluster
import uuid
import datetime

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra nodes
session = cluster.connect('ecommerce')  # Keyspace name

# Example table structure in Cassandra:
# CREATE TABLE cart (
#     cart_id uuid PRIMARY KEY,
#     user_id text,
#     session_id text,
#     product_id text,
#     quantity int,
#     created_at timestamp
# );

def add_to_cart(user_id=None, session_id=None, product_id=None, quantity=1):
    cart_id = uuid.uuid4()
    created_at = datetime.datetime.utcnow()
    query = """
        INSERT INTO cart (cart_id, user_id, session_id, product_id, quantity, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    session.execute(query, (cart_id, user_id, session_id, product_id, quantity, created_at))
    return cart_id

def get_cart_items(user_id=None, session_id=None):
    if user_id:
        query = "SELECT * FROM cart WHERE user_id=%s"
        return session.execute(query, (user_id,))
    elif session_id:
        query = "SELECT * FROM cart WHERE session_id=%s"
        return session.execute(query, (session_id,))
    else:
        return []
