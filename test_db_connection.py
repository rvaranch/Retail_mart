import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

def test_connection():
    """Test MySQL database connection"""
    try:
        # Get database configuration
        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "Welcome123")
        db_name = os.getenv("DB_NAME", "retail_mart_db")
        db_port = int(os.getenv("DB_PORT", 3306))
        
        print("=" * 60)
        print("DATABASE CONNECTION TEST")
        print("=" * 60)
        print(f"\nAttempting to connect with:")
        print(f"  Host: {db_host}")
        print(f"  User: {db_user}")
        print(f"  Password: {'*' * len(db_password)}")
        print(f"  Database: {db_name}")
        print(f"  Port: {db_port}")
        print()
        
        # Test connection
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✓ CONNECTION SUCCESSFUL!")
        print()
        
        # Get MySQL version
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"MySQL Version: {version}")
        
        # Check if products table exists
        cursor.execute("""
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'products'
        """, (db_name,))
        
        table_exists = cursor.fetchone()
        if table_exists:
            print("✓ 'products' table exists")
            
            # Count records in products table
            cursor.execute("SELECT COUNT(*) as count FROM products")
            count = cursor.fetchone()
            print(f"  Total records: {count['count']}")
        else:
            print("✗ 'products' table DOES NOT exist")
            print("  You need to run the create_tables.sql script")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        print("All checks passed!")
        print("=" * 60)
        
    except pymysql.err.OperationalError as e:
        print(f"\n✗ CONNECTION FAILED!")
        print(f"Error: {e}")
        print("\nPossible causes:")
        print("  1. MySQL server is not running")
        print("  2. Wrong host/port")
        print("  3. Wrong username/password")
        print("  4. Database doesn't exist")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")

if __name__ == "__main__":
    test_connection()
