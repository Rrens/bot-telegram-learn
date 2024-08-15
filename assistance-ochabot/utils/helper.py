import logging
from telegram import Bot

def is_whitelisted(telegram_id: int) -> bool:
    """
    Fungsi untuk memeriksa apakah ID Telegram ada di whitelist.
    """
    try:
        # Membaca file whitelist
        with open('whitelist.txt', 'r') as file:
            whitelist = file.read().splitlines()
        
        # Periksa apakah ID ada di whitelist
        if str(telegram_id) in whitelist:
            return True
        else:
            return False
    except FileNotFoundError:
        print('File whitelist.txt tidak ditemukan.')
        return False
    
def check_callback_query(update) -> bool:
    try:
        return getattr(update, 'callback_query', None) is None
    except Exception as e:
        print(f"Error: {e}")
        return True
    
def convert_safe_username(username):
    return username.replace('_', '\\_').replace('*', '\\*')
    
# def check_username_exists(username_telegram: str, bot: Bot) -> bool:
#     print('cekk')
#     try:
#         user_info = bot.get_chat(username_telegram)
#         print(f"USERNAME CEK ADA ATAU TIDAK {username_telegram}")
#         print(f"USER INFO CEK ADA ATAU TIDAK {user_info}")
#         # print(user_info)
        
#         if user_info:
#             print(f"Username {username_telegram} ditemukan. Nama: {user_info.first_name}")
#             return True
#         else:
#             print(f"Username {username_telegram} tidak ditemukan.")
#             return False

#     except Exception as e:
#         print(f"Error: {e}")
#         return False
    