import os
from dotenv import load_dotenv
from urllib.parse import quote_plus, urlparse, parse_qs, urlencode, urlunparse

# Load environment variables from .env file
load_dotenv()


def build_database_uri():
    """Build SQLAlchemy database URI from environment variables with safe driver prefix, query sanitization and encoding."""
    # Check for direct DATABASE_URL or MYSQL_URL (common on Render, Railway, Aiven, etc.)
    database_url = os.getenv('DATABASE_URL') or os.getenv('MYSQL_URL')
    if database_url:
        database_url = database_url.strip()
        # SQLAlchemy requires the mysql+pymysql dialect driver scheme
        if database_url.startswith('mysql://'):
            database_url = 'mysql+pymysql://' + database_url[len('mysql://'):]
        elif database_url.startswith('mysql2://'):
            database_url = 'mysql+pymysql://' + database_url[len('mysql2://'):]

        # Aiven and some other cloud providers append ?ssl-mode=REQUIRED which PyMySQL rejects as an unexpected kwarg.
        # Clean query parameters that PyMySQL does not accept natively in URL strings.
        parsed = urlparse(database_url)
        if parsed.query:
            query_params = parse_qs(parsed.query)
            for bad_key in ['ssl-mode', 'ssl_mode']:
                query_params.pop(bad_key, None)
            new_query = urlencode(query_params, doseq=True)
            database_url = urlunparse(parsed._replace(query=new_query))

        return database_url

    # Fallback to discrete parameters
    db_host = os.getenv('DB_HOST', 'localhost').strip()
    db_port = os.getenv('DB_PORT', '3306').strip()
    db_name = os.getenv('DB_NAME', 'polymer_recommendation_db').strip()
    db_user = os.getenv('DB_USER', 'root').strip()
    db_password = os.getenv('DB_PASSWORD', '')

    encoded_user = quote_plus(db_user)
    encoded_password = quote_plus(db_password)

    return f"mysql+pymysql://{encoded_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"


class Config:
    """Application configuration supporting both local development and cloud production."""

    # Environment detection
    ENVIRONMENT = os.getenv('ENVIRONMENT') or os.getenv('FLASK_ENV') or ('production' if os.getenv('RENDER') else 'development')
    IS_PRODUCTION = ENVIRONMENT.lower() in ['production', 'prod']

    # Secret key for Flask sessions and CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        if IS_PRODUCTION:
            raise RuntimeError(
                "SECRET_KEY environment variable is required in production! "
                "Generate a random string (e.g. `python -c 'import secrets; print(secrets.token_hex(32))'`) "
                "and set it in your hosting platform environment variables."
            )
        SECRET_KEY = 'dev-secret-key-change-in-production'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Build connection args (including SSL support for remote / Aiven MySQL databases)
    connect_args = {
        'connect_timeout': int(os.getenv('DB_CONNECT_TIMEOUT', '10'))
    }

    db_uri_lower = SQLALCHEMY_DATABASE_URI.lower()
    is_remote = not ('localhost' in db_uri_lower or '127.0.0.1' in db_uri_lower)
    enable_ssl = os.getenv('DB_SSL', '').lower() in ['1', 'true', 'required'] or 'aiven' in db_uri_lower or (is_remote and os.getenv('DB_SSL', '').lower() != 'false')

    if enable_ssl and is_remote:
        ssl_config = {'check_hostname': False}
        ca_path = os.getenv('DB_SSL_CA')
        if ca_path and os.path.exists(ca_path):
            ssl_config['ca'] = ca_path
        connect_args['ssl'] = ssl_config

    # Production database pool and connection settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', '280')),
        'pool_size': int(os.getenv('DB_POOL_SIZE', '5')),
        'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', '10')),
        'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', '30')),
        'connect_args': connect_args
    }

    # Debug mode (defaults to False in production)
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
