from urllib import response
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,CallbackContext

from datetime import datetime, timedelta 
from selenium import webdriver  
import time
import paramiko
import os
from io import BytesIO
from PIL import Image
from selenium.webdriver.chrome.options import Options

from bcid_syantic import chatid

os.environ['http_proxy'] = 'http://10.37.190.30:8080'
os.environ['HTTP_PROXY'] = 'http://10.37.190.30:8080'
os.environ['https_proxy'] = 'https://10.37.190.30:8080'
os.environ['HTTPS_PROXY'] = 'https://10.37.190.30:8080'

syanticbot = telegram.Bot('5090657370:AAHOCNlXVpC4bHNAbyotLeyWv_pSG2NW_U0') # saktiBot

def generate_text_report(response):
    pass

def send_message(text, chat_id):

    now = datetime.today() - timedelta(minutes=15)
    now = now.strftime("%d.%m.%Y %H:%M:%S")
    pattern_now = '%d.%m.%Y %H:%M:%S'
    epoch_now_ = int(time.mktime(time.strptime(now, pattern_now)))

    today_minday = datetime.today() - timedelta(hours=24)
    today_minday = today_minday.strftime("%d.%m.%Y %H:%M:%S")
    pattern_minday = '%d.%m.%Y %H:%M:%S'
    epoch_minday = int(time.mktime(time.strptime(today_minday, pattern_minday)))

    print('Process Screenshoot')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="10.41.202.57" , username="dimas", password="dimas10")

    stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/xfpJB9FGz/syantic-server-monitoring?orgId=11&var-origin_prometheus=&var-job=node_exporter&var-hostname=All&var-node=10.251.13.112:9100&var-device=All&var-interval=5m&var-maxmount=%2F&var-show_hostname=nocddb.localdomain&var-total=3&from={}050&to={}050&panelId=202&width=1200&height=220&tz=Asia%2FJakarta' -H 'Authorization: Bearer eyJrIjoicTJYdVFENjIxZjR0UUFuYVZpTDlNb0oxV0NSTzFpNVYiLCJuIjoic2NfZ2FyYWZhbmEiLCJpZCI6MTF9' --compressed > /home/dimas/baru/healthy_status/capture/syantic_table.png".format(epoch_minday,epoch_now_))
    lines = stdout.readlines()
    print("Syantic - Table screenshoot is successfully") 

    stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/3zJDjL44k/syantic-bot-monitoring?orgId=11&refresh=30s&var-host=All&var-node=10.251.13.112:9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=20&width=1000&height=500&tz=Asia%2FJakarta' -H 'Authorization: Bearer eyJrIjoicTJYdVFENjIxZjR0UUFuYVZpTDlNb0oxV0NSTzFpNVYiLCJuIjoic2NfZ2FyYWZhbmEiLCJpZCI6MTF9' --compressed > /home/dimas/baru/healthy_status/capture/syantic_cpu.png".format(epoch_minday,epoch_now_))
    lines = stdout.readlines()
    print("Syantic - CPU screenshoot is successfully") 

    stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/3zJDjL44k/syantic-bot-monitoring?orgId=11&refresh=30s&var-host=All&var-node=10.251.13.112:9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=6&width=1000&height=500&tz=Asia%2FJakarta' -H 'Authorization: Bearer eyJrIjoicTJYdVFENjIxZjR0UUFuYVZpTDlNb0oxV0NSTzFpNVYiLCJuIjoic2NfZ2FyYWZhbmEiLCJpZCI6MTF9' --compressed > /home/dimas/baru/healthy_status/capture/syantic_mem.png".format(epoch_minday,epoch_now_))
    lines = stdout.readlines()
    print("Syantic - Memory screenshoot is successfully") 

    stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/3zJDjL44k/syantic-bot-monitoring?orgId=11&refresh=30s&var-host=All&var-node=10.251.13.112:9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=8&width=1000&height=500&tz=Asia%2FJakarta' -H 'Authorization: Bearer eyJrIjoicTJYdVFENjIxZjR0UUFuYVZpTDlNb0oxV0NSTzFpNVYiLCJuIjoic2NfZ2FyYWZhbmEiLCJpZCI6MTF9' --compressed > /home/dimas/baru/healthy_status/capture/syantic_disk.png".format(epoch_minday,epoch_now_))
    lines = stdout.readlines()
    print("Syantic - Disk screenshoot is successfully")

    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-setuid-sandbox')

    # ###TABLE
    # driver_0 = webdriver.Chrome('/home/dimas/baru/syanticbot_v2/chromedriver', options=chrome_options)
    # driver_0.get('http://10.251.16.99:3000/grafana/d/xfpJB9FGz/internal-server-monitoring?orgId=9&viewPanel=185&var-origin_prometheus=&var-job=node_exporter3&var-hostname=All&var-node=10.251.13.112:9100&var-device=All&var-interval=5m&var-maxmount=%2F&var-show_hostname=nocddb.localdomain&var-total=2&from={}050&to={}050'.format(epoch_minday,epoch_now_))
    # driver_0.set_window_size(1200, 600)
    # driver_0.maximize_window()
    # time.sleep(1)
    # username = driver_0.find_element_by_name('user')
    # password = driver_0.find_element_by_name('password')
    # username.send_keys('admin')
    # password.send_keys('grafana')
    # driver_0.find_element_by_class_name("css-w9m50q-button").click()
    # time.sleep(3)
    # driver_0.execute_script("document.body.style.zoom='75%'")
    # time.sleep(3)
    # #screenshoot
    # screenPnG = driver_0.get_screenshot_as_png()
    # box = (42, 35, 1200, 210)#,kiri,atas,kanan,bawah
    # im = Image.open(BytesIO(screenPnG))
    # driver_ = im.crop(box)
    # driver_.save('/home/dimas/baru/healthy_status/capture/syantic_table.png', 'PNG', optimize=True, quality=95)
    # driver_0.close()
    # driver_0.quit()
    # print("Syantic - Table screenshoot is successfully") 
    # time.sleep(3)


    # ###CPU
    # driver_1 = webdriver.Chrome('/home/dimas/baru/syanticbot_v2/chromedriver', options=chrome_options)
    # driver_1.get('http://10.251.16.99:3000/grafana/d/3zJDjL44k/syantic-bot-monitoring?orgId=11&refresh=30s&var-host=All&var-node=10.251.13.112:9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&viewPanel=20&from={}045&to={}050'.format(epoch_minday,epoch_now_))
    # time.sleep(1)
    # username = driver_1.find_element_by_name('user')
    # password = driver_1.find_element_by_name('password')
    # username.send_keys('admin')
    # password.send_keys('grafana')
    # driver_1.find_element_by_class_name("css-w9m50q-button").click()
    # time.sleep(3)
    # driver_1.execute_script("document.body.style.zoom='85%'")
    # time.sleep(3)
    # #screenshoot
    # screenPnG = driver_1.get_screenshot_as_png()
    # box = (50, 80, 800, 600)#,kiri,atas,kanan,bawah
    # im = Image.open(BytesIO(screenPnG))
    # driver_1 = im.crop(box)
    # driver_1.save('/home/dimas/baru/healthy_status/capture/syantic_cpu.png', 'PNG', optimize=True, quality=95)
    # driver_1.close()
    # print("Syantic - CPU screenshoot is successfully") 

    # ###MEMORY
    # driver_2 = webdriver.Chrome('/home/dimas/baru/syanticbot_v2/chromedriver', options=chrome_options)
    # driver_2.get('http://10.251.16.99:3000/grafana/d/3zJDjL44k/syantic-bot-monitoring?orgId=11&refresh=30s&var-host=All&var-node=10.251.13.112:9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&viewPanel=6&from={}050&to={}050'.format(epoch_minday,epoch_now_))
    # time.sleep(1)
    # #login
    # username = driver_2.find_element_by_name('user')
    # password = driver_2.find_element_by_name('password')
    # username.send_keys('admin')
    # password.send_keys('grafana')
    # driver_2.find_element_by_class_name("css-w9m50q-button").click()
    # time.sleep(3)
    # driver_2.execute_script("document.body.style.zoom='85%'")
    # time.sleep(3)
    # #screenshoot
    # screenPnG = driver_2.get_screenshot_as_png()
    # box = (50, 80, 800, 600)#,kiri,atas,kanan,bawah
    # im = Image.open(BytesIO(screenPnG))
    # driver_2 = im.crop(box)
    # driver_2.save('/home/dimas/baru/healthy_status/capture/syantic_mem.png', 'PNG', optimize=True, quality=95)
    # driver_2.close()
    # print("Syantic - Memory screenshoot is successfully") 

    # ###DISK
    # driver_3 = webdriver.Chrome('/home/dimas/baru/syanticbot_v2/chromedriver', options=chrome_options)
    # driver_3.get('http://10.251.16.99:3000/grafana/d/3zJDjL44k/syantic-bot-monitoring?orgId=11&refresh=30s&var-host=All&var-node=10.251.13.112:9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&viewPanel=8&from={}050&to={}050'.format(epoch_minday,epoch_now_))
    # time.sleep(1)
    # #login
    # username = driver_3.find_element_by_name('user')
    # password = driver_3.find_element_by_name('password')
    # username.send_keys('admin')
    # password.send_keys('grafana')
    # driver_3.find_element_by_class_name("css-w9m50q-button").click()
    # time.sleep(3)
    # driver_3.execute_script("document.body.style.zoom='85%'")
    # time.sleep(3)
    # #screenshoot
    # screenPnG = driver_3.get_screenshot_as_png()
    # box = (50, 80, 800, 600)#,kiri,atas,kanan,bawah
    # im = Image.open(BytesIO(screenPnG))
    # driver_3 = im.crop(box)
    # driver_3.save('/home/dimas/baru/healthy_status/capture/syantic_disk.png', 'PNG', optimize=True, quality=95)
    # driver_3.close()

    # print("Syantic - Disk screenshoot is successfully")


    # os.system("/home/dimas/baru/bin/python /home/dimas/baru/kill_process/kill_chrome.py")


    #1 HOSTNAME
    user = open('/home/dimas/baru/healthy_status/log_file/syantic/log_hostname.txt','r')
    health = user.read().split('\n')
    #
    health_0 = health[0]
    health_0 = health_0.split(':')
    health_host0 = health_0[2]

    #
    health_1 = health[1]
    health_1 = health_1.split(':')
    health_host1 = health_1[2]
    #
    health_2 = health[2]
    health_2 = health_2.split(':')
    health_host2 = health_2[2]
   
   
    #2 IP ADDRESS
    user = open('/home/dimas/baru/healthy_status/log_file/syantic/log_ip.txt','r')
    health = user.read().split('\n')
    #
    health_0 = health[0]
    health_0 = health_0.split(':')
    health_ip_0 = health_0[2]
    #
    health_1 = health[1]
    health_1 = health_1.split(':')
    health_ip_1 = health_1[2]
    #
    health_2 = health[2]
    health_2 = health_2.split(':')
    health_ip_2 = health_2[2]
    

    # #3 STATUS
    # user = open('/home/dimas/baru/healthy_status/log_file/syantic/log_status.txt','r')
    # health = user.read().split('\n')
    # #
    # health_0 = health[0]
    # health_0 = health_0.split(':')
    # # health_0 = health_0[1]
    # print(health_0)
    # health_status_0 = health_0.replace('Health_Status = ','')
    # #
    # health_1 = health[1]
    # health_1 = health_1.split(':')
    # health_1 = health_1[1]
    # health_status_1 = health_1.replace('Health_Status = ','')
    # #
    # health_2 = health[2]
    # health_2 = health_2.split(':')
    # health_2 = health_2[1]
    # health_status_2 = health_2.replace('Health_Status = ','')
    
    

    #4 Kernel Version
    user = open('/home/dimas/baru/healthy_status/log_file/syantic/log_kernel.txt','r')
    health = user.read().split('\n')
    #
    health_0 = health[0]
    health_0 = health_0.split(':')
    health_kernel_0 = health_0[2]
    #
    health_1 = health[1]
    health_1 = health_1.split(':')
    health_kernel_1 = health_1[2]
    #
    health_2 = health[2]
    health_2 = health_2.split(':')
    health_kernel_2 = health_2[2]
    
    
    ##5 Uptime
    user = open('/home/dimas/baru/healthy_status/log_file/syantic/log_uptime.txt','r')
    health = user.read().split('\n')
    #
    health_0 = health[0]
    health_0 = health_0.split(':')
    health_uptime_0 = health_0[2]
    #
    health_1 = health[1]
    health_1 = health_1.split(':')
    health_uptime_1 = health_1[2]
    #
    health_2 = health[2]
    health_2 = health_2.split(':')
    health_uptime_2 = health_2[2]
    
    


    # #6 Last Reboot Time
    user = open('/home/dimas/baru/healthy_status/log_file/syantic/log_last_reboot.txt','r')
    health = user.read().split('\n')
    #
    health_0 = health[0]
    health_0 = health_0.split(':')
    health_reboot_date_0 = health_0[2]
    # health_rebootsec_0 = health_0[3]
    # health_reboot_date_0 = health_rebootmin_0+':'+health_rebootsec_0
    # #
    health_1 = health[1]
    health_1 = health_1.split(':')
    health_reboot_date_1 = health_1[2]
    # health_rebootsec_1 = health_1[3]
    # health_reboot_date_1 = health_rebootmin_1+':'+health_rebootsec_1
    # #
    health_2 = health[2]
    health_2 = health_2.split(':')
    health_reboot_date_2 = health_2[2]
    # health_rebootsec_2 = health_2[3]
    # health_reboot_date_2 = health_rebootmin_2+':'+health_rebootsec_2
    
    


    # #7 Update Check 
    user = open('/home/dimas/baru/healthy_status/log_file/syantic/log_update_check.txt','r')
    health = user.read().split('\n')
    #
    health_0 = health[0]
    health_0 = health_0.split(':')
    health_min_0 = health_0[2]
    health_sec_0 = health_0[3]
    health_date_0 = health_min_0+':'+health_sec_0
    #
    health_1 = health[1]
    health_1 = health_1.split(':')
    health_min_1 = health_1[2]
    health_sec_1 = health_1[3]
    health_date_1 = health_min_1+':'+health_sec_1
    #
    health_2 = health[2]
    health_2 = health_2.split(':')
    health_min_2 = health_2[2]
    health_sec_2 = health_2[3]
    health_date_2 = health_min_2+':'+health_sec_2
    
    



    chatid = '-811946004'
    now = datetime.today()
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    date_time_morining = now.strftime("%H") == '07'
    # print(date_time_morining)
    date_time_afternoon = now.strftime("%H") == '17'
    if date_time_morining is True:
        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        pin = syanticbot.sendMessage(chatid, text='📆 *Morning Daily Health Check* ➞ _{}_'.format(date_time),parse_mode=telegram.ParseMode.MARKDOWN)
    
        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendDocument(chat_id = "-811946004", document=open('/home/dimas/baru/healthy_status/status/syantic/health_status-{}.txt'.format(health_ip_0).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host0,health_ip_0).replace(' ',''), caption='Healthy Check Server :\n\nApplication : SYANTIC\nHostname : {}\nIP Address : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host0,health_ip_0,health_kernel_0,health_uptime_0,health_reboot_date_0,health_date_0))

        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendDocument(chat_id = "-811946004", document=open('/home/dimas/baru/healthy_status/status/syantic/health_status-{}.txt'.format(health_ip_1).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host1,health_ip_1).replace(' ',''), caption='Healthy Check Server :\n\nApplication : SYANTIC\nHostname : {}\nIP Address : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host1,health_ip_1,health_kernel_1,health_uptime_1,health_reboot_date_1,health_date_1))

        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendDocument(chat_id = "-811946004", document=open('/home/dimas/baru/healthy_status/status/syantic/health_status-{}.txt'.format(health_ip_2).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host2,health_ip_2).replace(' ',''), caption='Healthy Check Server :\n\nApplication : SYANTIC\nHostname : {}\nIP Address : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host2,health_ip_2,health_kernel_2,health_uptime_2,health_reboot_date_2,health_date_2))

        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/syantic_table.png', 'rb'),caption='♻️ Healthy Check All Server SYANTIC\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nRegards\nOCHABOT & Team')
        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/syantic_cpu.png', 'rb'),caption='♻️ Healthy check CPU used SYANTIC\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')
        syanticbot.sendChatAction(chat_id = "-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/syantic_mem.png', 'rb'),caption='♻️ Healthy check Memory used SYANTIC\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')
        syanticbot.sendChatAction(chat_id = "-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/syantic_disk.png', 'rb'),caption='♻️ Healthy check Disk used SYANTIC\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')



        syanticbot.pin_chat_message(chatid, pin.message_id)
        print('Sukses Terkirim')

    elif date_time_afternoon is True:
        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        pin = syanticbot.sendMessage(chatid, text='📆 *Afternoon Daily Health Check* ➞ _{}_'.format(date_time),parse_mode=telegram.ParseMode.MARKDOWN)
    
        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendDocument(chat_id = "-811946004", document=open('/home/dimas/baru/healthy_status/status/syantic/health_status-{}.txt'.format(health_ip_0).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host0,health_ip_0).replace(' ',''), caption='Healthy Check Server :\n\nApplication : SYANTIC\nHostname : {}\nIP Address : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host0,health_ip_0,health_kernel_0,health_uptime_0,health_reboot_date_0,health_date_0))

        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendDocument(chat_id = "-811946004", document=open('/home/dimas/baru/healthy_status/status/syantic/health_status-{}.txt'.format(health_ip_1).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host1,health_ip_1).replace(' ',''), caption='Healthy Check Server :\n\nApplication : SYANTIC\nHostname : {}\nIP Address : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host1,health_ip_1,health_kernel_1,health_uptime_1,health_reboot_date_1,health_date_1))

        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendDocument(chat_id = "-811946004", document=open('/home/dimas/baru/healthy_status/status/syantic/health_status-{}.txt'.format(health_ip_2).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host2,health_ip_2).replace(' ',''), caption='Healthy Check Server :\n\nApplication : SYANTIC\nHostname : {}\nIP Address : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host2,health_ip_2,health_kernel_2,health_uptime_2,health_reboot_date_2,health_date_2))

        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/syantic_table.png', 'rb'),caption='♻️ Healthy Check All Server SYANTIC\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nRegards\nOCHABOT & Team')
        syanticbot.sendChatAction(chat_id="-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/syantic_cpu.png', 'rb'),caption='♻️ Healthy check CPU used SYANTIC\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')
        syanticbot.sendChatAction(chat_id = "-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/syantic_mem.png', 'rb'),caption='♻️ Healthy check Memory used SYANTIC\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')
        syanticbot.sendChatAction(chat_id = "-811946004",action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/syantic_disk.png', 'rb'),caption='♻️ Healthy check Disk used SYANTIC\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')

        syanticbot.pin_chat_message(chatid, pin.message_id)
        print('Sukses Terkirim')



for region in chatid:
    if ( isinstance(chatid[region], list) ):
        for chat_id in chatid[region]:
            send_message(generate_text_report(response), chat_id)
    else:
        send_message(generate_text_report(response), chatid[region])
