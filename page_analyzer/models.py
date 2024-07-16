import requests
from page_analyzer import parse_url
from psycopg2.extras import RealDictCursor
from page_analyzer.config import Config
import psycopg2


def make_connection():
    try:
        return psycopg2.connect(Config.DATABASE_URL,
                                cursor_factory=RealDictCursor)
    except psycopg2.Error as exception:
        return exception


def add_new_url(url):
    with (
        make_connection() as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute('INSERT INTO urls (name) VALUES %s',
                       (url,))
        connection.commit()


def check_exist_url(url):
    with (
        make_connection() as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute('SELECT * FROM urls WHERE name = %s', (url,))
        response = cursor.fetchone()
        if response:
            return True
        return False


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
        return response


def add_new_check(url, url_id):
    with (
        make_connection() as connection,
        connection.cursor() as cursor,
    ):
        try:
            status_code = parse_url.get_status_code(url)
            attributes = parse_url.get_attributes_content(url)
            cursor.execute('INSERT INTO urls_checks '
                           '(url_id, status_code, h1,'
                           ' title, description)'
                           'VALUES (%s, %s, %s, %s, %s)',
                           (url_id, status_code, attributes.get('h1', ''),
                            attributes.get('title', ''),
                            attributes.get('meta', '')))
            connection.commit()
            return True
        except requests.exceptions.RequestException:
            return False


def get_checks_url(url_id):
    with (
        make_connection() as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute('SELECT * FROM urls_checks '
                       'WHERE url_id = %s ORDER BY id DESC', (url_id,))
        response = cursor.fetchall()
        return response


def get_checks_urls():
    with (
        make_connection() as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute('SELECT '
                       'urls.id as url_id, '
                       'urls.name as name, '
                       'status_code, '
                       'max(urls_checks.created_at) as last_checked '
                       'FROM urls_checks '
                       'RIGHT JOIN urls ON urls.id = urls_checks.url_id '
                       'GROUP BY status_code, urls.id , urls.name '
                       'ORDER BY url_id DESC ')

        response = cursor.fetchall()
        return response
