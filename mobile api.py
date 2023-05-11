from playwright.sync_api import sync_playwright
from gwmailpy import GwApi
import random, json, time, re, os

api = GwApi(timeout=30)

def get_coords():
    min_lat, max_lat = 47.3, 55.1
    min_lon, max_lon = 5.5, 15.1

    latitude = round(random.uniform(min_lat, max_lat), 6)
    longitude = round(random.uniform(min_lon, max_lon), 6)

    return (latitude, longitude)

def get_agent():
    ios_version = "15.1.1"
    safari_version = "15.1"
    mobile_version = "15E148"

    agent = f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) AppleWebKit/{safari_version} (KHTML, like Gecko) Version/{ios_version} Mobile/{mobile_version} Safari/{safari_version}"
    #not used while playwright generates one
    return agent

def run(playwright):
    iphone_13 = playwright.devices['iPhone 13']
    browser = playwright.webkit.launch(headless=False)
    latitude, longitude = get_coords()
    context = browser.new_context(**iphone_13, geolocation = {"longitude": longitude, "latitude": latitude}, locale = "de-DE")
    page = context.new_page()
    email = api.load_mail()
    print(f"got {email}")
    page.goto("https://www.instagram.com/")
    page.get_by_role("button", name="Alle Cookies erlauben").click()
    page.get_by_role("button", name="Registrieren").click()
    page.get_by_role("switch", name="E-Mail-Adresse").click()
    page.get_by_placeholder("E-Mail-Adresse").fill(email)
    page.get_by_role("button", name="Weiter").click()
    print("getting code")
    time.sleep(15)
    for mail in api.load_inbox():
        content = api.get_message_value(mail['id'])
        code = re.findall(r'\b\d{6}\b', content)[0]
        raw_code = r"{}".format(code)
        print(raw_code.strip())
        page.get_by_placeholder("Bestätigungscode").fill(raw_code.strip())
        page.get_by_role("button", name="Weiter").click()
        page.get_by_placeholder("Vollständiger Name").fill("voll name")
        page.get_by_placeholder("Passwort").click()
        page.get_by_placeholder("Passwort").press("CapsLock")
        page.get_by_placeholder("Passwort").fill("P")
        page.get_by_placeholder("Passwort").press("CapsLock")
        page.get_by_placeholder("Passwort").fill("Passwor81273!")
        page.get_by_role("button", name="Weiter").click()
        page.get_by_role("combobox", name="Jahr:").select_option("2000")
        page.get_by_role("button", name="Weiter").click()
        time.sleep(30)

with sync_playwright() as playwright:
    os.system("cls")
    run(playwright)