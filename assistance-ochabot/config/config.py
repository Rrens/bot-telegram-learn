import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
}

REPORT_MENU, MENU_REGISTRATION, REQ_TICKET, REQ_APP_ERROR, REQ_TICKET_ADD, MENU, CREATE_USER = range(7)


END = range(1)

# Dapatkan nama variabel yang ingin diekspor
__all__ = [name for name in globals() if not name.startswith('_') and name != 'db_config'] + ['db_config']
# __all__ = [name for name in globals() if not name.startswith('_')]