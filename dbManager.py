import mysql.connector

# TODO
#conn = None 

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'dbManager',
    'password': '1234',
    'database': 'cleisthenes_database'
}

# Database setup function
def setup_database():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = conn.cursor()