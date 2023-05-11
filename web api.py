from playwright.sync_api import Playwright, sync_playwright, expect
from gwmailpy import GwApi
import json, time, re, os

api = GwApi(timeout=30)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(locale = "de-DE")
    page = context.new_page()
    page = context.new_page()
    email = api.load_mail()
    print("got mail " + email)
    page.goto("https://www.instagram.com/accounts/emailsignup/")
    page.get_by_role("button", name="Alle Cookies erlauben").click()
    page.get_by_label("Handynummer oder E-Mail-Adresse").click()
    page.get_by_label("Handynummer oder E-Mail-Adresse").fill(email)
    page.get_by_label("Vollständiger Name").click()
    page.get_by_label("Vollständiger Name").fill("manuel heins")
    page.get_by_label("Benutzername").click()
    page.get_by_label("Benutzername").fill("uaserasdj123123")
    page.get_by_label("Passwort").click()
    page.get_by_label("Passwort").fill("pasdjasdjhb12312")
    page.get_by_role("button", name="Weiter").click()
    page.get_by_role("combobox", name="Monat:").select_option("1")
    page.get_by_role("combobox", name="Tag:").select_option("1")
    page.get_by_role("combobox", name="Jahr:").select_option("1990")
    page.get_by_role("button", name="Weiter").click()
    page.get_by_placeholder("Bestätigungscode").click()
    print("getting code")
    time.sleep(13)
    for mail in api.load_inbox():
        content = api.get_message_value(mail['id'])
        code = re.findall(r'\b\d{6}\b', content)[0]
        raw_code = r"{}".format(code)
        print(raw_code.strip())
        page.get_by_label("Bestätigungscode").fill(raw_code.strip())
        page.get_by_role("button", name="Weiter").click()
        time.sleep(10)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    os.system("cls")
    run(playwright)