from playwright.sync_api import Playwright, sync_playwright, expect
from selectolax.parser import HTMLParser
import time


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    time.sleep(5)
    page.goto("https://udelistmo.instructure.com/login?needs_cookies=1")
    time.sleep(5)
    page.get_by_role("link", name="Iniciar sesión").click()
    page.locator("#ddlCategoria").select_option("2")
    page.get_by_placeholder("  Cédula").click()
    page.get_by_placeholder("  Cédula").press("CapsLock")
    page.get_by_placeholder("  Cédula").click()
    page.get_by_placeholder("  Cédula").fill("E-8-197382")
    page.get_by_placeholder("  Contraseña").click()
    page.get_by_placeholder("  Contraseña").press("CapsLock")
    page.get_by_placeholder("  Contraseña").fill("")
    page.get_by_placeholder("  Contraseña").press("CapsLock")
    page.get_by_placeholder("  Contraseña").fill("")
    page.get_by_role("button", name="Ingresar").click()
    page.get_by_role("button", name="Cursos").click()

    time.sleep(2)

    #Get HTML
    html = page.content()
    tree = HTMLParser(html)

    # Get the list of courses
    cursos = tree.css("ul ul.css-1t5l7tc-view--block-list")

    # Goes through the list of courses and clicks on each one
    for curso in cursos:
        for a_tag in curso.css("a"):
            curso_name = a_tag.text(deep=True)
            time.sleep(2)
            page.get_by_role("link", name=curso_name, exact=True).click()
            time.sleep(2)
            page.get_by_role("link", name="Tareas").click()
            time.sleep(2)
            print(tree.text())
            time.sleep(10)
            page.get_by_role("button", name="Cursos", exact=True).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
