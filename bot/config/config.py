import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
}

# REPORT_MENU, MENU_REGISTRATION, REQ_TICKET, REQ_APP_ERROR, REQ_TICKET_ADD, MENU, REPORT_PROBLEM = range(7)
END, MENU, MAIN_MENU, MENU_REPORT, REPORT_PROBLEM, PROFESSIONAL_TEAM, REPORT_STATUS, MESSAGE_BROADCAST, MAKE_ADMIN, DELETE_USER, DOWNLOAD_REPORT_TICKET, TICKET_LIST, CASE_ESCALATION = range(13)

(
    END,
    CREATE_TICKET, 
    ACCEPTANCE, 
    APPLICATION_ERROR, 
    DEPLOYMENT, 
    PROCESS, 
    ISSUE_PARTIAL_BAUT, 
    LOGIN, 
    DASHBOARD, 
    TASKLIST, 
    PLANNING, 
    KNOWLEDGE, 
    ELIGIBILITY_CHECK, 
    BUDGET, 
    OTHER_PROBLEM, 
    REQUEST_TICKET_END_APP_ERR_1, 
    REQUEST_TICKET_END_APP_ERR_2, 
    REQUEST_TICKET_END_APP_ERR_3
) = range(18)

# APPLICATION_ERROR
# REQUEST_TICKET_END_APP_ERR_1, REQUEST_TICKET_END_APP_ERR_2, REQUEST_TICKET_END_APP_ERR_3 = range(3)

# Dapatkan nama variabel yang ingin diekspor
__all__ = [name for name in globals() if not name.startswith('_') and name != 'db_config'] + ['db_config']
# __all__ = [name for name in globals() if not name.startswith('_')]