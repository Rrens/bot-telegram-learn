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

from bcid_unem import chatid
# from bc_id import chatid


# os.environ['http_proxy'] = 'http://10.37.190.30:8080'
# os.environ['HTTP_PROXY'] = 'http://10.37.190.30:8080'
# os.environ['https_proxy'] = 'https://10.37.190.30:8080'
# os.environ['HTTPS_PROXY'] = 'https://10.37.190.30:8080'

os.environ['HTTPS_PROXY'] = 'https://10.59.211.19:8080'

syanticbot = telegram.Bot('5090657370:AAHOCNlXVpC4bHNAbyotLeyWv_pSG2NW_U0') # saktiBot

def generate_text_report(response):
    pass

def send_message(text, chat_id):

    now = datetime.today() - timedelta(minutes=15)
    now = now.strftime("%d.%m.%Y %H:%M:%S")
    pattern_now = '%d.%m.%Y %H:%M:%S'
    epoch_now = int(time.mktime(time.strptime(now, pattern_now)))


    today_minday = datetime.today() - timedelta(hours=24)
    today_minday = today_minday.strftime("%d.%m.%Y %H:%M:%S")
    pattern_minday = '%d.%m.%Y %H:%M:%S'
    epoch_minday = int(time.mktime(time.strptime(today_minday, pattern_minday)))
    
    now_2 = datetime.today() - timedelta(minutes=15)
    epoch_now_2 = int(now_2.timestamp() * 1000)  # Konversi ke milidetik

    # Ambil waktu 24 jam yang lalu
    today_minday_2 = datetime.today() - timedelta(hours=24)
    epoch_minday_2 = int(today_minday_2.timestamp() * 1000)  # Konversi ke milidetik

    # image = "curl 'http://10.251.16.99:3000/grafana/render/d-solo/n2qv--zVz/alert-unem-monitoring?orgId=15&refresh=5s&var-host=All&var-node=unempapp1.telkomsel.co.id%3A9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=8&width=1000&height=500&tz=Asia%2FBangkok' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_disk.png".format(epoch_minday,epoch_now)
    # image = "curl 'http://10.251.16.99:3000/grafana/render/d-solo/xfpJB9FGz/alert-unem-monitoring?orgId=15&refresh=5s&var-host=All&var-node=unempapp1.telkomsel.co.id%3A9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=185&width=1000&height=500&tz=Asia%2FBangkok' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_disk.png".format(epoch_minday,epoch_now) # BISA
    # image = "curl 'curl 'http://10.251.16.99:3000/grafana/render/d-solo/xfpJB9FGz/alert-unem-monitoring?orgId=15&refresh=5s&var-host=All&var-node=unempapp1.telkomsel.co.id%3A9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=185&width=1000&height=500&tz=Asia%2FBangkok' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_disk.png".format(epoch_minday,epoch_now)
    # image = "curl 'http://10.251.16.99:3000/grafana/render/d-solo/xfpJB9FGz/unem-server?orgId=15&from={}&to={}&panelId=185&width=1000&height=500&tz=Asia%2FJakarta' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_table.png".format(epoch_minday,epoch_now)
    image = "curl 'http://10.251.16.99:3000/grafana/d/xfpJB9FGz/unem-server?orgId=15' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_table-testing.png".format(epoch_minday,epoch_now)
    print(image)
    print('Process Screenshoot')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="10.41.202.57" , username="dimas", password="dimas10")

    stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/xfpJB9FGz/unem-server?orgId=15&var-origin_prometheus=&var-job=node_exporter&var-hostname=All&var-node=unempapp1.telkomsel.co.id%3A9100&var-device=All&var-interval=5m&var-maxmount=%2Fapps&var-show_hostname=unempapp1.telkomsel.co.id&var-total=16&from={}050&to={}050&panelId=185&width=1600&height=735&tz=Asia%2FBangkok' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_table.png".format(epoch_minday,epoch_now))
    lines = stdout.readlines()
    print("UNEM - Table screenshoot is successfully") 

    stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/n2qv--zVz/alert-unem-monitoring?orgId=15&refresh=5s&var-host=All&var-node=unempapp1.telkomsel.co.id%3A9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=20&width=1000&height=500&tz=Asia%2FBangkok' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_cpu.png".format(epoch_minday,epoch_now))
    lines = stdout.readlines()
    print("UNEM - CPU screenshoot is successfully") 

    stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/n2qv--zVz/alert-unem-monitoring?orgId=15&refresh=5s&var-host=All&var-node=unempapp1.telkomsel.co.id%3A9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=6&width=1000&height=500&tz=Asia%2FBangkok' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_mem.png".format(epoch_minday,epoch_now))
    lines = stdout.readlines()
    print("UNEM - Memory screenshoot is successfully") 
    
    stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/n2qv--zVz/alert-unem-monitoring?orgId=15&refresh=5s&&var-host=All&var-node=unempapp1.telkomsel.co.id%3A9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}&to={}&panelId=8&width=1000&height=500&tz=Asia%2FBangkok' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_disk.png".format(epoch_minday_2,epoch_now_2))
    lines = stdout.readlines()
    print("UNEM - Disk screenshoot is successfully")
    # stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/n2qv--zVz/alert-unem-monitoring?orgId=15&refresh=5s&var-host=All&var-node=unempapp1.telkomsel.co.id%3A9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=8&width=1000&height=500&tz=Asia%2FBangkok' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_disk.png".format(epoch_minday,epoch_now))
    # stdin, stdout, stderr = client.exec_command("curl 'http://10.251.16.99:3000/grafana/render/d-solo/xfpJB9FGz/alert-unem-monitoring?orgId=15&refresh=5s&var-host=All&var-node=unempapp1.telkomsel.co.id%3A9100&var-interval=5m&var-hostname=&var-job=node_exporter&var-origin=All&from={}050&to={}050&panelId=185&width=1000&height=500&tz=Asia%2FBangkok' -H 'Authorization: Bearer eyJrIjoiMjIxVGhDQ0c5RUU4S0JiTE9CV2c2dTRLSkxwQ0Y2R04iLCJuIjoic2NfZ3JhZmFuYSIsImlkIjoxNX0=' --compressed > /home/dimas/baru/healthy_status/capture/unem_disk.png".format(epoch_minday,epoch_now))
    # print(f"epoch_minday: {epoch_minday}")
    # print(f"epoch_now: {epoch_now}")



    # #1 HOSTNAME
    # user = open('/home/dimas/baru/healthy_status/log_file/fiola/log_hostname.txt','r')
    # health = user.read().split('\n')
    # #
    # health_0 = health[0]
    # health_0 = health_0.split(':')
    # health_host0 = health_0[2]
    # #
    # health_1 = health[1]
    # health_1 = health_1.split(':')
    # health_host1 = health_1[2]
    # #
    # health_2 = health[2]
    # health_2 = health_2.split(':')
    # health_host2 = health_2[2]
    
    # health_3 = health[3]
    # health_3 = health_3.split(':')
    # health_host3 = health_3[2]
    # #
    # health_4 = health[4]
    # health_4 = health_4.split(':')
    # health_host4 = health_4[2]
    # #
    # health_5 = health[5]
    # health_5 = health_5.split(':')
    # health_host5 = health_5[2]
    # #
    # health_6 = health[6]
    # health_6 = health_6.split(':')
    # health_host6 = health_6[2]
    # #
    # health_7 = health[7]
    # health_7 = health_7.split(':')
    # health_host7 = health_7[2]
    # #
    # health_8 = health[8]
    # health_8 = health_8.split(':')
    # health_host8 = health_8[2]
    # #
    # health_9 = health[9]
    # health_9 = health_9.split(':')
    # health_host9 = health_9[2]
    # #
    # health_10 = health[10]
    # health_10 = health_10.split(':')
    # health_host10 = health_10[2]
    # #
    # health_11 = health[11]
    # health_11 = health_11.split(':')
    # health_host11 = health_11[2]
   
    # #2 IP ADDRESS
    # user = open('/home/dimas/baru/healthy_status/log_file/fiola/log_ip.txt','r')
    # health = user.read().split('\n')
    # #
    # health_0 = health[0]
    # health_0 = health_0.split(':')
    # health_ip_0 = health_0[2]
    # #
    # health_1 = health[1]
    # health_1 = health_1.split(':')
    # health_ip_1 = health_1[2]
    # #
    # health_2 = health[2]
    # health_2 = health_2.split(':')
    # health_ip_2 = health_2[2]
    # #
    # health_3 = health[3]
    # health_3 = health_3.split(':')
    # health_ip_3 = health_3[2]
    # #
    # health_4 = health[4]
    # health_4 = health_4.split(':')
    # health_ip_4 = health_4[2]
    # #
    # health_5 = health[5]
    # health_5 = health_5.split(':')
    # health_ip_5 = health_5[2]
    # #
    # health_6 = health[6]
    # health_6 = health_6.split(':')
    # health_ip_6 = health_6[2]
    # #
    # health_7 = health[7]
    # health_7 = health_7.split(':')
    # health_ip_7 = health_7[2]
    # #
    # health_8 = health[8]
    # health_8 = health_8.split(':')
    # health_ip_8 = health_8[2]
    # #
    # health_9 = health[9]
    # health_9 = health_9.split(':')
    # health_ip_9 = health_9[2]
    # #
    # health_10 = health[10]
    # health_10 = health_10.split(':')
    # health_ip_10 = health_10[2]
    # #
    # health_11 = health[11]
    # health_11 = health_11.split(':')
    # health_ip_11 = health_11[2]

    

    # #3 STATUS
    # user = open('/home/dimas/baru/healthy_status/log_file/fiola/log_status.txt','r')
    # health = user.read().split('\n')
    # #
    # health_0 = health[0]
    # health_0 = health_0.split(':')
    # health_0 = health_0[1]
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
    # #
    # health_3 = health[3]
    # health_3 = health_3.split(':')
    # health_3 = health_3[1]
    # health_status_3 = health_3.replace('Health_Status = ','')
    # #
    # health_4 = health[4]
    # health_4 = health_4.split(':')
    # health_4 = health_4[1]
    # health_status_4 = health_4.replace('Health_Status = ','')
    # #
    # health_5 = health[5]
    # health_5 = health_5.split(':')
    # health_5 = health_5[1]
    # health_status_5 = health_5.replace('Health_Status = ','')
    # #
    # health_6 = health[6]
    # health_6 = health_6.split(':')
    # health_6 = health_6[1]
    # health_status_6 = health_6.replace('Health_Status = ','')
    # #
    # health_7 = health[7]
    # health_7 = health_7.split(':')
    # health_7 = health_7[1]
    # health_status_7 = health_7.replace('Health_Status = ','')
    # #
    # health_8 = health[8]
    # health_8 = health_8.split(':')
    # health_8 = health_8[1]
    # health_status_8 = health_8.replace('Health_Status = ','')
    # #
    # health_9 = health[9]
    # health_9 = health_9.split(':')
    # health_9 = health_9[1]
    # health_status_9 = health_9.replace('Health_Status = ','')
    # #
    # health_10 = health[10]
    # health_10 = health_10.split(':')
    # health_10 = health_10[1]
    # health_status_10 = health_10.replace('Health_Status = ','')
    # #
    # health_11 = health[11]
    # health_11 = health_11.split(':')
    # health_11 = health_11[1]
    # health_status_11 = health_11.replace('Health_Status = ','')
    
    

    # #4 Kernel Version
    # user = open('/home/dimas/baru/healthy_status/log_file/fiola/log_kernel.txt','r')
    # health = user.read().split('\n')
    # #
    # health_0 = health[0]
    # health_0 = health_0.split(':')
    # health_kernel_0 = health_0[2]
    # #
    # health_1 = health[1]
    # health_1 = health_1.split(':')
    # health_kernel_1 = health_1[2]
    # #
    # health_2 = health[2]
    # health_2 = health_2.split(':')
    # health_kernel_2 = health_2[2]
    # #
    # health_3 = health[3]
    # health_3 = health_3.split(':')
    # health_kernel_3 = health_3[2]
    # #
    # health_4 = health[4]
    # health_4 = health_4.split(':')
    # health_kernel_4 = health_4[2]
    # #
    # health_5 = health[5]
    # health_5 = health_5.split(':')
    # health_kernel_5 = health_5[2]
    # #
    # health_6 = health[6]
    # health_6 = health_6.split(':')
    # health_kernel_6 = health_6[2]
    # #
    # health_7 = health[7]
    # health_7 = health_7.split(':')
    # health_kernel_7 = health_7[2]
    # #
    # health_8 = health[8]
    # health_8 = health_8.split(':')
    # health_kernel_8 = health_8[2]
    # #
    # health_9 = health[9]
    # health_9 = health_9.split(':')
    # health_kernel_9 = health_9[2]
    # #
    # health_10 = health[10]
    # health_10 = health_10.split(':')
    # health_kernel_10 = health_10[2]
    # #
    # health_11 = health[11]
    # health_11 = health_11.split(':')
    # health_kernel_11 = health_11[2]
    
    
    # ##5 Uptime
    # user = open('/home/dimas/baru/healthy_status/log_file/fiola/log_uptime.txt','r')
    # health = user.read().split('\n')
    # #
    # health_0 = health[0]
    # health_0 = health_0.split(':')
    # health_uptime_0 = health_0[2]
    # #
    # health_1 = health[1]
    # health_1 = health_1.split(':')
    # health_uptime_1 = health_1[2]
    # #
    # health_2 = health[2]
    # health_2 = health_2.split(':')
    # health_uptime_2 = health_2[2]
    # #
    # health_3 = health[3]
    # health_3 = health_3.split(':')
    # health_uptime_3 = health_3[2]
    # #
    # health_4 = health[4]
    # health_4 = health_4.split(':')
    # health_uptime_4 = health_4[2]
    # #
    # health_5 = health[5]
    # health_5 = health_5.split(':')
    # health_uptime_5 = health_5[2]
    # #
    # health_6 = health[6]
    # health_6 = health_6.split(':')
    # health_uptime_6 = health_6[2]
    # #
    # health_7 = health[7]
    # health_7 = health_7.split(':')
    # health_uptime_7 = health_7[2]
    # #
    # health_8 = health[8]
    # health_8 = health_8.split(':')
    # health_uptime_8 = health_8[2]
    # #
    # health_9 = health[9]
    # health_9 = health_9.split(':')
    # health_uptime_9 = health_9[2]
    # #
    # health_10 = health[10]
    # health_10 = health_10.split(':')
    # health_uptime_10 = health_10[2]
    # #
    # health_11 = health[11]
    # health_11 = health_11.split(':')
    # health_uptime_11 = health_11[2]
    
    


    # # #6 Last Reboot Time
    # user = open('/home/dimas/baru/healthy_status/log_file/fiola/log_last_reboot.txt','r')
    # health = user.read().split('\n')
    # #
    # health_0 = health[0]
    # health_0 = health_0.split(':')
    # health_rebootmin_0 = health_0[2]
    # health_rebootsec_0 = health_0[3]
    # health_reboot_date_0 = health_rebootmin_0+':'+health_rebootsec_0
    # #
    # health_1 = health[1]
    # health_1 = health_1.split(':')
    # health_rebootmin_1 = health_1[2]
    # health_rebootsec_1 = health_1[3]
    # health_reboot_date_1 = health_rebootmin_1+':'+health_rebootsec_1
    # #
    # health_2 = health[2]
    # health_2 = health_2.split(':')
    # health_rebootmin_2 = health_2[2]
    # health_rebootsec_2 = health_2[3]
    # health_reboot_date_2 = health_rebootmin_2+':'+health_rebootsec_2
    #  #
    # health_3 = health[3]
    # health_3 = health_3.split(':')
    # health_rebootmin_3 = health_3[2]
    # health_rebootsec_3 = health_3[3]
    # health_reboot_date_3 = health_rebootmin_3+':'+health_rebootsec_3
    # #
    # health_4 = health[4]
    # health_4 = health_4.split(':')
    # health_rebootmin_4 = health_4[2]
    # health_rebootsec_4 = health_4[3]
    # health_reboot_date_4 = health_rebootmin_4+':'+health_rebootsec_4
    # #
    # health_5 = health[5]
    # health_5 = health_5.split(':')
    # health_rebootmin_5 = health_5[2]
    # health_rebootsec_5 = health_5[3]
    # health_reboot_date_5 = health_rebootmin_5+':'+health_rebootsec_5

    # #
    # health_6 = health[6]
    # health_6 = health_6.split(':')
    # health_rebootmin_6 = health_6[2]
    # health_rebootsec_6 = health_6[3]
    # health_reboot_date_6 = health_rebootmin_6+':'+health_rebootsec_6

    # #
    # health_7 = health[7]
    # health_7 = health_7.split(':')
    # health_rebootmin_7 = health_7[2]
    # health_rebootsec_7 = health_7[3]
    # health_reboot_date_7 = health_rebootmin_7+':'+health_rebootsec_7
    # #
    # health_8 = health[8]
    # health_8 = health_8.split(':')
    # health_rebootmin_8 = health_8[2]
    # health_rebootsec_8 = health_8[3]
    # health_reboot_date_8 = health_rebootmin_8+':'+health_rebootsec_8
    # #
    # health_9 = health[9]
    # health_9 = health_9.split(':')
    # health_rebootmin_9 = health_9[2]
    # health_rebootsec_9 = health_9[3]
    # health_reboot_date_9 = health_rebootmin_9+':'+health_rebootsec_9
    # #
    # health_10 = health[10]
    # health_10 = health_10.split(':')
    # health_rebootmin_10 = health_10[2]
    # health_rebootsec_10 = health_10[3]
    # health_reboot_date_10 = health_rebootmin_10+':'+health_rebootsec_10
    # #
    # health_reboot_date_11 = health[11]
    # # health_11 = health_11.split(':')
    # # health_rebootmin_11 = health_11[2]
    # # health_rebootsec_11 = health_11[3]
    # # health_reboot_date_11 = health_rebootmin_11+':'+health_rebootsec_11
    
    


    # # #7 Update Check 
    # user = open('/home/dimas/baru/healthy_status/log_file/fiola/log_update_check.txt','r')
    # health = user.read().split('\n')
    # #
    # health_0 = health[0]
    # health_0 = health_0.split(':')
    # health_min_0 = health_0[2]
    # health_sec_0 = health_0[3]
    # health_date_0 = health_min_0+':'+health_sec_0
    # #
    # health_1 = health[1]
    # health_1 = health_1.split(':')
    # health_min_1 = health_1[2]
    # health_sec_1 = health_1[3]
    # health_date_1 = health_min_1+':'+health_sec_1
    # #
    # health_2 = health[2]
    # health_2 = health_2.split(':')
    # health_min_2 = health_2[2]
    # health_sec_2 = health_2[3]
    # health_date_2 = health_min_2+':'+health_sec_2
    # #
    # health_3 = health[3]
    # health_3 = health_3.split(':')
    # health_min_3 = health_3[2]
    # health_sec_3 = health_3[3]
    # health_date_3 = health_min_3+':'+health_sec_3
    # #
    # health_4 = health[4]
    # health_4 = health_4.split(':')
    # health_min_4 = health_4[2]
    # health_sec_4 = health_4[3]
    # health_date_4 = health_min_4+':'+health_sec_4
    # #
    # health_5 = health[5]
    # health_5 = health_5.split(':')
    # health_min_5 = health_5[2]
    # health_sec_5 = health_5[3]
    # health_date_5 = health_min_5+':'+health_sec_5
    # #
    # health_6 = health[6]
    # health_6 = health_6.split(':')
    # health_min_6 = health_6[2]
    # health_sec_6 = health_6[3]
    # health_date_6 = health_min_6+':'+health_sec_6
    # #
    # health_7 = health[7]
    # health_7 = health_7.split(':')
    # health_min_7 = health_7[2]
    # health_sec_7 = health_7[3]
    # health_date_7 = health_min_7+':'+health_sec_7
    # #
    # health_8 = health[8]
    # health_8 = health_8.split(':')
    # health_min_8 = health_8[2]
    # health_sec_8 = health_8[3]
    # health_date_8 = health_min_8+':'+health_sec_8
    # #
    # health_9 = health[9]
    # health_9 = health_9.split(':')
    # health_min_9 = health_9[2]
    # health_sec_9 = health_9[3]
    # health_date_9 = health_min_9+':'+health_sec_9
    # #
    # health_10 = health[10]
    # health_10 = health_10.split(':')
    # health_min_10 = health_10[2]
    # health_sec_10 = health_10[3]
    # health_date_10 = health_min_10+':'+health_sec_10
    # #
    # health_11 = health[11]
    # health_11 = health_11.split(':')
    # health_min_11 = health_11[2]
    # health_sec_11 = health_11[3]
    # health_date_11 = health_min_11+':'+health_sec_11
    
    



    chatid = '-922185904'
    # chatid = '462124845'
    now = datetime.today()
    date_time = now.strftime("%d-%B-%Y, %H:%M:%S WIB")
    date_time_morining = now.strftime("%H") == '07'
    # print(date_time_morining)
    date_time_afternoon = now.strftime("%H") == '17'
    if date_time_morining is True:
        syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        pin = syanticbot.sendMessage(chatid, text='📆 *Morning Daily Health Check* ➞ _{}_'.format(date_time),parse_mode=telegram.ParseMode.MARKDOWN)
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_0).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host0,health_ip_0).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host0,health_ip_0,health_status_0,health_kernel_0,health_uptime_0,health_reboot_date_0,health_date_0))

        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_1).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host1,health_ip_1).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host1,health_ip_1,health_status_1,health_kernel_1,health_uptime_1,health_reboot_date_1,health_date_1))

        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_2).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host2,health_ip_2).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {} (10.175.1.168)\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host2,health_ip_2,health_status_2,health_kernel_2,health_uptime_2,health_reboot_date_2,health_date_2))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_3).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host3,health_ip_3).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host3,health_ip_3,health_status_3,health_kernel_3,health_uptime_3,health_reboot_date_3,health_date_3))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_4).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host4,health_ip_4).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host4,health_ip_4,health_status_4,health_kernel_4,health_uptime_4,health_reboot_date_4,health_date_4))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_5).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host5,health_ip_5).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host5,health_ip_5,health_status_5,health_kernel_5,health_uptime_5,health_reboot_date_5,health_date_5))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_6).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host6,health_ip_6).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host6,health_ip_6,health_status_6,health_kernel_6,health_uptime_6,health_reboot_date_6,health_date_6))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_7).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host7,health_ip_7).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host7,health_ip_7,health_status_7,health_kernel_7,health_uptime_7,health_reboot_date_7,health_date_7))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_8).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host8,health_ip_8).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host8,health_ip_8,health_status_8,health_kernel_8,health_uptime_8,health_reboot_date_8,health_date_8))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_9).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host9,health_ip_9).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host9,health_ip_9,health_status_9,health_kernel_9,health_uptime_9,health_reboot_date_9,health_date_9))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_10).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host10,health_ip_10).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host10,health_ip_10,health_status_10,health_kernel_10,health_uptime_10,health_reboot_date_10,health_date_10))

        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_11).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host11,health_ip_11).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {} (10.53.199.200)\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host11,health_ip_11,health_status_11,health_kernel_11,health_uptime_11,health_reboot_date_11,health_date_11))

        syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/unem_table.png', 'rb'),caption='♻️ Healthy Check All Server UNEM Monitoring\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nRegards\nOCHABOT & Team')
        syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/unem_cpu.png', 'rb'),caption='♻️ Healthy check CPU used UNEM\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')
        syanticbot.sendChatAction(chat_id = chatid,action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/unem_mem.png', 'rb'),caption='♻️ Healthy check Memory used UNEM\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')
        syanticbot.sendChatAction(chat_id = chatid,action=telegram.ChatAction.TYPING)
        syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/unem_disk.png', 'rb'),caption='♻️ Healthy check Disk used UNEM\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')

        syanticbot.pin_chat_message(chatid, pin.message_id)
        print('Sukses Terkirim')

    elif date_time_afternoon is True:
        syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        pin = syanticbot.sendMessage(chatid, text='📆 *Afternoon Daily Health Check* ➞ _{}_'.format(date_time),parse_mode=telegram.ParseMode.MARKDOWN)
        
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_0).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host0,health_ip_0).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host0,health_ip_0,health_status_0,health_kernel_0,health_uptime_0,health_reboot_date_0,health_date_0))

        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_1).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host1,health_ip_1).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host1,health_ip_1,health_status_1,health_kernel_1,health_uptime_1,health_reboot_date_1,health_date_1))

        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_2).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host2,health_ip_2).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {} (10.175.1.168)\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host2,health_ip_2,health_status_2,health_kernel_2,health_uptime_2,health_reboot_date_2,health_date_2))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_3).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host3,health_ip_3).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host3,health_ip_3,health_status_3,health_kernel_3,health_uptime_3,health_reboot_date_3,health_date_3))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_4).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host4,health_ip_4).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host4,health_ip_4,health_status_4,health_kernel_4,health_uptime_4,health_reboot_date_4,health_date_4))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_5).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host5,health_ip_5).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host5,health_ip_5,health_status_5,health_kernel_5,health_uptime_5,health_reboot_date_5,health_date_5))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_6).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host6,health_ip_6).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host6,health_ip_6,health_status_6,health_kernel_6,health_uptime_6,health_reboot_date_6,health_date_6))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_7).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host7,health_ip_7).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host7,health_ip_7,health_status_7,health_kernel_7,health_uptime_7,health_reboot_date_7,health_date_7))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_8).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host8,health_ip_8).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host8,health_ip_8,health_status_8,health_kernel_8,health_uptime_8,health_reboot_date_8,health_date_8))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_9).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host9,health_ip_9).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host9,health_ip_9,health_status_9,health_kernel_9,health_uptime_9,health_reboot_date_9,health_date_9))
    
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_10).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host10,health_ip_10).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {}\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host10,health_ip_10,health_status_10,health_kernel_10,health_uptime_10,health_reboot_date_10,health_date_10))

        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendDocument(chat_id = chatid, document=open('/home/dimas/baru/healthy_status/status/fiola/health_status-{}.txt'.format(health_ip_11).replace(' ',''),'rb'), filename="healthy_status-{}-{}.txt".format(health_host11,health_ip_11).replace(' ',''), caption='Healthy Check Server :\n\nApplication : Fiola Monitoring\nHostname : {}\nIP Address : {} (10.53.199.200)\nStatus : {}\nKernel Version : {}\nUptime : {}\nLast Reboot Time : {}\nUpdate Check : {}\n\nThank You\nRegards\nOCHABOT & Team'.format(health_host11,health_ip_11,health_status_11,health_kernel_11,health_uptime_11,health_reboot_date_11,health_date_11))

        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/unem_table.png', 'rb'),caption='♻️ Healthy Check All Server UNEM Monitoring\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nRegards\nOCHABOT & Team')
        # syanticbot.sendChatAction(chat_id=chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/unem_cpu.png', 'rb'),caption='♻️ Healthy check CPU used UNEM\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')
        # syanticbot.sendChatAction(chat_id = chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/unem_mem.png', 'rb'),caption='♻️ Healthy check Memory used UNEM\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')
        # syanticbot.sendChatAction(chat_id = chatid,action=telegram.ChatAction.TYPING)
        # syanticbot.sendPhoto(chat_id,open('/home/dimas/baru/healthy_status/capture/unem_disk.png', 'rb'),caption='♻️ Healthy check Disk used UNEM\n\nℹ️ Note graph :\n├ Time ranges : Last 24 Hours\n└ Interval : 5 Minutes\n\nCondition is Good ✅ if value under thresholds (<80%)\n\nRegards\nOCHABOT & Team')
        # syanticbot.pin_chat_message(chatid, pin.message_id)
        print('Sukses Terkirim')



for region in chatid:
    if ( isinstance(chatid[region], list) ):
        for chat_id in chatid[region]:
            send_message(generate_text_report(response), chat_id)
    else:
        send_message(generate_text_report(response), chatid[region])
