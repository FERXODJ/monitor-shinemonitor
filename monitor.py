from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
# Ajustes Iniciales
ChromeOptions = Options()
DriverPath = r"C:\Users\duvely_huiza\OneDrive - MDS Telecom CA\Escritorio\Python Eduardo\chromedriver-win64\chromedriver.exe"
service = Service(DriverPath)
 
# Iniciar Navegador
driver = webdriver.Chrome(service=service, options=ChromeOptions)
url = "https://www.shinemonitor.com/index_en.html?1757165053874"
driver.get(url)
driver.maximize_window()
 
# Espera para el campo de usuario
wait = WebDriverWait(driver, 30)  # Espera hasta 30 segundos
usuario = wait.until(EC.presence_of_element_located((By.XPATH, '//input [@placeholder="Enter one user name"]')))
contraseña = driver.find_element(By.XPATH, '//input [@id="mypassword"]')
 
# Ingresa las credenciales
usuario.send_keys("COR_energia")
contraseña.send_keys("mds12345678")
 
# Encuentra y hace clic en el botón de login
boton_login = driver.find_element(By.ID, "loginbtn")
boton_login.click()
 
# Espera a que el menú desplegable sea clickeable
menu_desplegable = wait.until(EC.element_to_be_clickable((By.ID, "checkedPlant")))
menu_desplegable.click()
 
# Espera a que la opción de la planta sea visible y luego clickea
selecc_planta = wait.until(EC.visibility_of_element_located((By.ID, "plant_214436")))
selecc_planta.click()
 
# ---
# Espera a que la superposición "API Application" desaparezca o a que el elemento sea clickeable
# Esta es la parte crucial.
# 1. Espera a que el tab de gestión de dispositivos sea clickeable.
tab_Device_Management = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#plantDevice"]')))
tab_Device_Management.click()
 
# Opcional: Si el span es un modal, podrías necesitar cerrarlo primero.
# Por ejemplo, si hay un botón de cerrar:
# try:
#     cerrar_modal = wait.until(EC.element_to_be_clickable((By.XPATH, 'xpath_del_boton_cerrar')))
#     cerrar_modal.click()
#     # Después de cerrarlo, espera a que el tab sea clickeable
#     tab_Device_Management = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#plantDevice"]')))
#     tab_Device_Management.click()
# except:
#     # Si no hay modal, continúa
#     pass
# ---
 
# Espera para la selección del inversor
selecc_inverter = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Rbs Mecedores')))
selecc_inverter.click()
 
# ...existing code...
from selenium.common.exceptions import StaleElementReferenceException

for _ in range(3):  # Intenta hasta 3 veces
    try:
        tab_inverter_Detail = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#inverterDetail"]')))
        tab_inverter_Detail.click()
        break
    except StaleElementReferenceException:
        time.sleep(1)

# Coloca aquí el bloque para extraer la tabla
time.sleep(2)  # Espera extra para asegurar que la tabla cargue

tabla = wait.until(EC.presence_of_element_located((By.XPATH, '//table[@id="invDetailTable"]')))
filas = tabla.find_elements(By.XPATH, './/tbody/tr')[:1]

print(f"Filas encontradas: {len(filas)}")  # Debe estar fuera del bucle

datos = []
nombre_monitor = "Rbs Mecedores"
for fila in filas:
    columnas = fila.find_elements(By.TAG_NAME, 'td')
    fila_datos = [col.text for col in columnas]
    print(fila_datos)
    # Agrega el nombre del monitor al inicio de la fila
    datos.append([nombre_monitor] + fila_datos)

encabezados = tabla.find_elements(By.XPATH, './/thead/tr/th')
headers = [th.text for th in encabezados]
headers = ["Nombre del Monitor"] + headers

df = pd.DataFrame(datos, columns=headers)
df.to_csv(f"{nombre_monitor}.csv", index=False, encoding='utf-8-sig')

input("Presiona Enter para cerrar el navegador...")
driver.quit()
 