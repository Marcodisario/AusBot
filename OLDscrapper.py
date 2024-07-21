from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import asyncio

load_dotenv()


# VARIABLES A CAMBIAR 
CAMPUS_URL = os.getenv("CAMPUS_URL")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")

# Verificar si las variables de entorno están definidas
if not CAMPUS_URL or not USER_EMAIL or not USER_PASSWORD:
    raise ValueError("Asegúrate de que las variables de entorno CAMPUS_URL, USER_EMAIL y USER_PASSWORD estén definidas")

# Initialize the Chrome driver with options
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode if desired
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Variables globales para guardar datos scrapeados

materias = []

notificaciones = []

# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def wait_and_interact_with_element(xpath, text_content=""):
    """
    Esta función espera a que un elemento sea clickeable y luego interactúa con él.
    Si se proporciona un text_content, se ingresará en el elemento, de lo contrario, se hará clic en el elemento.
    :param xpath: El xpath del elemento con el que interactuar.
    :param text_content: El texto a ingresar en el elemento, si corresponde.
    :return: Ninguno
    """
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    if text_content == "":
        element.click()
    else:
        element.send_keys(text_content)

def microsoft_login():
    # Esta función inicia el proceso de login en el campus virtual.
    # Toma en cuenta el login externo de microsoft. Modificar en caso de que tu universidad no lo ultilice.
    # Ayuda en discord => .lorenn
    print("🔒 Ingresando...")
    driver.get(CAMPUS_URL)

    # Wait for the login button to be clickable and then click it
    wait_and_interact_with_element('//*[@id="login"]/div/a')

    # Wait for the email input field to be clickable and then enter the user's email
    wait_and_interact_with_element('//*[@id="i0116"]', USER_EMAIL)

    # Wait for the next button to be clickable and then click it
    wait_and_interact_with_element('//*[@id="idSIButton9"]')

    print("🔐 Login de microsoft...")
    # Wait for the username input field to be clickable and then enter the user's email again
    wait_and_interact_with_element('//*[@id="username"]', USER_EMAIL)

    # Wait for the password input field to be clickable and then enter the user's password
    wait_and_interact_with_element('//*[@id="password"]', USER_PASSWORD)

    # Wait for the submit credentials button to be clickable and then click it
    wait_and_interact_with_element('//*[@id="SubmitCreds"]')

    print("🔓 We're In")

def seleccionar_propuesta(n=1):
    try:
        print(f"📚 Seleccionando propuesta académica número {n}")
        driver.execute_script(f"document.querySelector('#js-dropdown-menu-carreras li:nth-child({n}) a').click();")
    except Exception as e:
        print(f"Error al seleccionar propuesta académica: {e}")

def iterate_over_sons(url_location, parent_xpath):
    driver.get(url_location)
    output = []
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, parent_xpath)))
    elements = driver.find_elements(By.XPATH, parent_xpath)

    for element in elements:
        output.append(element.text)
        print(element.text)

    return output

def scrape_subjects():
    driver.get("https://siu.austral.edu.ar/portal/cursada/")
    parent_xpath = '//*[@id="js-listado-materias"]/ul/li/a'
    output = {}
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, parent_xpath)))
    elements = driver.find_elements(By.XPATH, parent_xpath)

    for element in elements:
        output[element.text] = {
            'url': element.get_attribute('href')
        }

    for subject_name, subject_data in output.items():
        driver.get(subject_data['url'])
        time.sleep(0.3)
        try:
            cupos = driver.find_element(By.XPATH, '//*[@id="comisiones"]/li/div/ul/li[1]/div[1]/div[2]').text
        except:
            cupos = ''
        try:
            description = driver.find_element(By.XPATH, '//*[@id="comisiones"]/li/div/ul/div/div[2]').text
        except:
            description = ''
        output[subject_name] = {
            'url': subject_data['url'],
            'cupos': cupos,
            'description': description,
        }

    return output

def scrape_data():
    print("🔄 Scraping de datos...")
    driver.get('https://siu.austral.edu.ar')
    microsoft_login()
    seleccionar_propuesta(2)

    # Scrape de materias
    materias = scrape_subjects()

    print(f"MATERIAAAAS {materias}")
    # Scrape de notificaciones
    # driver.get('https://siu.austral.edu.ar/portal/mensajes')
    # wait_and_interact_with_element('/html/body/div[1]/div/div/div[2]/div[1]/div/div/ul/li[2]/a')

    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lista_mensajes"]/table/tbody')))
    # message_elements = driver.find_elements(By.XPATH, '//*[@id="lista_mensajes"]/table/tbody/tr')
    # global notificaciones
    # notificaciones = []
    # for message_element in message_elements:
    #     if "leido" in message_element.get_attribute('class'):
    #         notificaciones.append(f"[no_leído] {message_element.text}")
    #     else:
    #         notificaciones.append(f"[leido] {message_element.text}")

    # print("📊 Datos scrapeados y almacenados.")

    # return materias, notificaciones

# materias, notificaciones = scrape_data()

scrape_data()
print(f"DATOS SCRAPEADOS => {materias}, {notificaciones}")


# def scrape_materias():
#     microsoft_login()
#     seleccionar_propuesta(2)
#     return iterate_over_sons('https://siu.austral.edu.ar/portal/cursada/', '//*[@id="js-listado-materias"]/ul/li/a')


# def scrape_materias():
#     microsoft_login()
#     seleccionar_propuesta(2)
#     materias = iterate_over_sons('https://siu.austral.edu.ar/portal/cursada/', '//*[@id="js-listado-materias"]/ul/li/a')
#     return materias

# microsoft_login()
# seleccionar_propuesta(2)
# materias = iterate_over_sons('https://siu.austral.edu.ar/portal/cursada/','//*[@id="js-listado-materias"]/ul/li/a')
# print(materias)