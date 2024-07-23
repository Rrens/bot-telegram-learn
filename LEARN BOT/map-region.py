from pprint import pprint
import telegram
import requests, os, sys
import emojis
import requests
import json
import emojis
import folium

from datetime import datetime, timedelta 
from folium.plugins import MiniMap, minimap
from PIL import Image
from selenium.webdriver.chrome.options import Options
from telegram import update
from webdriver_manager import chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from pymongo import MongoClient
from urllib3 import disable_warnings
from argparse import ArgumentParser
from requests import get as fetch
from pprint import pprint
from folium import Map, Marker
from folium.features import DivIcon
from time import sleep

# sys.path.append("./crontab_auto")
from region_map_chatid import chatid_map

# os.environ['http_proxy'] = 'http://10.37.190.30:8080'
# os.environ['HTTP_PROXY'] = 'http://10.37.190.30:8080'
os.environ['https_proxy'] = 'https://10.37.190.30:8080'
os.environ['HTTPS_PROXY'] = 'https://10.37.190.30:8080'

syanticbot = telegram.Bot('1087167235:AAEPeLuJX0i2g6JNwcAXEMRsQUAUNk1beG0') # syanticbot
token_bot = '6782119374:AAGhKVO2AU10YumwgB7q2I_z9YooyyYqgfU' #SWFMBOT DEV

def generate_text_report(response):
	map_incident = Map(location=[-0.789275, 113.9213257], tiles=None, zoom_start=6, min_zoom=1, max_zoom=14)

	reg_1 = region == "REGIONAL1"
	reg_2 = region == "REGIONAL2"
	reg_3 = region == "REGIONAL3"
	reg_12 = region == "REGIONAL3.5"
	reg_4 = region == "REGIONAL4"
	reg_5 = region == "REGIONAL5"
	reg_6 = region == "REGIONAL6"
	reg_7 = region == "REGIONAL7"
	reg_8 = region == "REGIONAL8"
	reg_9 = region == "REGIONAL9"
	reg_10 = region == "REGIONAL10"
	reg_11 = region == "REGIONAL11"
	# print(reg_2)
	if reg_1 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL SUMBAGUT").add_to(map_incident)
	if reg_2 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL SUMBAGSEL").add_to(map_incident)
	if reg_3 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL JABOTABEK INNER").add_to(map_incident)
	if reg_12 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL JABOTABEK OUTER").add_to(map_incident)
	if reg_4 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL JABAR").add_to(map_incident)
	if reg_5 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL JATENG").add_to(map_incident)
	if reg_6 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL JATIM").add_to(map_incident)
	if reg_7 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL BALNUS").add_to(map_incident)
	if reg_8 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL KALIMANTAN").add_to(map_incident)
	if reg_9 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL SULAWESI").add_to(map_incident)
	if reg_10 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL SUMBAGTENG").add_to(map_incident)
	if reg_11 is True: 
		folium.TileLayer("openstreetmap", name="REGIONAL PUMA").add_to(map_incident)
	for ne in response:
		info5 = folium.FeatureGroup(name="Last Update : {}".format(response1['last_update'])).add_to(map_incident)
		info = folium.FeatureGroup(name="Total Impact NE: {} NE of {} NE".format(response1['total_impact_ne'],response1['total_sysinfo_ne'])).add_to(map_incident)
		info1 = folium.FeatureGroup(name="Total Impact SITE: {} SITE of {} SITE".format(response1['total_impact_site'],response1['total_sysinfo_site'])).add_to(map_incident)
		info2 = folium.FeatureGroup(control=True,show=True,overlay=True,name="4G ON : {}%".format(100 - response1['4G_percentage'])).add_to(map_incident)
		info3 = folium.FeatureGroup(name="3G ON : {}%".format(100 - response1['3G_percentage'])).add_to(map_incident)
		info4 = folium.FeatureGroup(name="2G ON: {}%".format(100 - response1['2G_percentage'])).add_to(map_incident)
		fx_flag_do = ne['flag'] == "DOWN"
		fx_flag_re = ne['flag'] == "RECOVER"
		if fx_flag_do:
			# print("NE ID: ",ne['ne_id'], '| coordinates: ',ne['location']['coordinates'])
			Marker([ne['location']['coordinates'][1], ne['location']['coordinates'][0]],  popup=ne['ne_id'], icon=DivIcon(icon_size=(25,25),icon_anchor=(12,12),html="<div style='height: 15px; width: 15px; background-color: #FF0000; color:black; font-size:12px; line-height:14px; padding-top:5px; border-radius: 50%; text-align: center'></div>")).add_to(map_incident)
		if fx_flag_re:
			# print("NE ID: ",ne['ne_id'], '| coordinates: ',ne['location']['coordinates'])
			Marker([ne['location']['coordinates'][1], ne['location']['coordinates'][0]],  popup=ne['ne_id'], icon=DivIcon(icon_size=(25,25),icon_anchor=(12,12),html="<div style='height: 15px; width: 15px; background-color: #00ff5f; color:black; font-size:12px; line-height:14px; padding-top:5px; border-radius: 50%; text-align: center'></div>")).add_to(map_incident)
				# exit()
	fx = response == '[]'
	# print(response)
	if response:
		map_incident.fit_bounds([[ne['location']['coordinates'][1], ne['location']['coordinates'][0]]], max_zoom=7)
		folium.LayerControl(collapsed=False).add_to(map_incident)
		minimap = MiniMap(toggle_display=True)
		map_incident.add_child(minimap)
		map_incident.save('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html')
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument('window-size=1920x1080')
		# try:
		driver = webdriver.Chrome(executable_path='/home/dimas/baru/chromedriver', chrome_options=options)
		dir_path = os.path.dirname(os.path.realpath(__file__))
		# print(dir_path)
		driver.get('file:///home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html')
		# driver.execute_script("document.body.style.zoom='140%'")
		driver.maximize_window()
		sleep(5)
		# driver.get_screenshot_as_file('/home/dimas/baru/telebot/script/crontab_image/map_site_down_nsa.png')
		driver.save_screenshot("/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png")
		print('success')

		driver.close()
		driver.quit()
		print('kill chromedriver active')
		os.system("/home/dimas/baru/bin/python /home/dimas/baru/kill_process/kill_chrome.py")	
	else:
		print('Gagal')

def send_message(text, chat_id):
	
	reg1 = region == 'REGIONAL1'
	reg2 = region == 'REGIONAL2'
	reg3 = region == 'REGIONAL3'
	reg12 = region == 'REGIONAL3.5'
	reg4 = region == 'REGIONAL4'
	reg5 = region == 'REGIONAL5'
	reg6 = region == 'REGIONAL6'
	reg7 = region == 'REGIONAL7'
	reg8 = region == 'REGIONAL8'
	reg9 = region == 'REGIONAL9'
	reg10 = region == 'REGIONAL10'
	reg11 = region == 'REGIONAL11'
	if reg1 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region SUMBAGUT*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region SUMBAGUT")
	elif reg2 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region SUMBAGSEL*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region SUMBAGSEL")
	elif reg3 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region JABOTABEK INNER*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region JABOTABEK INNER")
	elif reg12 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region JABOTABEK OUTER*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region JABOTABEK OUTER")
	elif reg4 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region JABAR*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region JABAR")
	elif reg5 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region JATENG*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region JATENG")
	elif reg6 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region JATIM*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region JATIM")
	elif reg7 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region BALNUS*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region BALNUS")
	elif reg8 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region KALIMANTAN*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region KALIMANTAN")
	elif reg9 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region SULAWESI*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region SULAWESI")
	elif reg10 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region SUMBAGTENG*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region SUMBAGTENG")
	elif reg11 is True:
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendMessage(chat_id = chat_id, text = '📍 *Berikut MAP Site Down Region PUMA*', parse_mode = telegram.ParseMode.MARKDOWN)
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendPhoto(chat_id=chat_id ,photo=open('/home/dimas/baru/telebot/script/crontab_image/map_site_down_region.png', 'rb'))
		syanticbot.sendChatAction(chat_id = chat_id, action = telegram.ChatAction.TYPING)
		syanticbot.sendDocument(chat_id, document=open('/home/dimas/baru/telebot/script/crontab_image/Map_Site_Down_Region.html', 'rb'),caption="Silahkan klik untuk melihat Map Site Down Region PUMA")


URL= "http://10.54.28.211/api/qc/realtime/ne"
URL1= "http://10.54.28.211/api/qc/summary"
# url1= fetch("http://10.54.28.211/api/qc/summary?region=REGIONAL{}".format(region),verify=False).json()

for region in chatid_map:
    if(chatid_map[region] != ""):
        proxies = {"no_proxy": "*"}
        response = requests.get(url=URL, proxies=proxies, params={"region": region}).json()
        response1 = requests.get(url=URL1, proxies=proxies, params={"region": region}).json()

        print('send to bot on group {}'.format(region))
        if ( isinstance(chatid_map[region], list) ):
            for chat_id in chatid_map[region]:
                send_message(generate_text_report(response), chat_id)
        else:
            send_message(generate_text_report(response), chatid_map[region])

