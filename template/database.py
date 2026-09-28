import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "artificial_intelligence",
    "port": 3306
}


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database connection error:", e)

    return None


def save_poem(topic, mood, poem):
    connection = get_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO poems (topic, mood, poem)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (topic, mood, poem))
        connection.commit()

        return True

    except Error as e:
        print("Error saving poem:", e)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def get_all_poems():
    connection = get_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id, topic, mood, poem, created_at
            FROM poems
            ORDER BY id DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Error as e:
        print("Error fetching poems:", e)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def delete_poem(poem_id):
    connection = get_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = "DELETE FROM poems WHERE id = %s"
        cursor.execute(query, (poem_id,))
        connection.commit()

        return True

    except Error as e:
        print("Error deleting poem:", e)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()