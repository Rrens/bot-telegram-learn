import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
}

(
    MENU,
    SEARCH_APP,
    FIND_APP,
    SHOW_FIND_APP,
    MAIN_MENU,
    FORM,
    DOWNLOAD_FORM,
    UPLOAD_FORM,
    HANDLE_UPLOAD_FORM
) = range(9)

__all__ = [name for name in globals() if not name.startswith('_') and name != 'db_config'] + ['db_config']