from psycopg2.extras import RealDictCursor
from page_analyzer.config import Config
from datetime import date
import psycopg2


def make_connection():
    try:
        return psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)
    except psycopg2.Error as exception:
        return exception


def add_new_url(url):
    with (
        make_connection() as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)', (url, date.today()))
        connection.commit()


# def check_exist_url(url):
#     with (
#         make_connection() as connection,
#         connection.cursor() as cursor,
#     ):
#         cursor.execute('SELECT * FROM urls WHERE name = %s', (url,))
#         response = cursor.fetchone()
#         print(response)
#
#         if response:
#             return response
#         return False

def get_url_id(url):
    with (
        make_connection() as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute('SELECT id FROM urls WHERE name = %s', (url,))
        response = cursor.fetchone()
        return response['id']


def get_url_items(url_id):
    with (
        make_connection() as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
        response = cursor.fetchone()
        print(response)
        return response
