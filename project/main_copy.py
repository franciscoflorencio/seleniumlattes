from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv
import numpy as np

# https://sites.google.com/chromium.org/driver
#abre o chromedriver
service = Service(executable_path="chromedriver.bin")
driver = webdriver.Chrome()

#entra no buscalattes e maximiza a janela
driver.get("https://buscatextual.cnpq.br/buscatextual/busca.do")
driver.maximize_window()

wait = WebDriverWait(driver, 10)

#seta a variável original_window como a janela original
original_window = driver.current_window_handle

buscaavancada = driver.find_element(By.CSS_SELECTOR, "div#tit_simples.control-bar-top")
buscaavancadabutton = buscaavancada.find_element(By.TAG_NAME, 'a')
buscaavancadabutton.click()

input_element = driver.find_element(By.CSS_SELECTOR, "textarea.input-text.min-height")
input_element.clear()
input_element.send_keys('(oncológicos AND injetáveis), (oncology AND injectable), (câncer AND injetáveis), (cancer AND injectables), (antineoplásicos AND injetáveis), (injectable AND neoplasm), (injetáveis AND neoplasia)')

time.sleep(30)

#espera até q a página de pesquisa seja carregada
WebDriverWait(driver, 5).until(
EC.presence_of_element_located((By.CSS_SELECTOR, "div[class = 'resultado']"))
)

#cria dicionario
dictionary = {}

#encontra a quantidade de curriculos presentes na pagina
el = driver.find_element(By.CSS_SELECTOR, "div[class = 'resultado']")
listsize = el.find_elements(By.TAG_NAME, "li")

time.sleep(2)
#encontra número de paginas encontrados na busca
numero = driver.find_element(By.CSS_SELECTOR, "div[class = 'tit_form'] b").text
numero = int(numero)
numero = int(np.ceil(numero/10))

perfis = 0
traffic = 1
first = False
for j in range(numero):
    if j > 10:
        first = True
    if traffic % 10 == 0 and first == True:
        page = driver.find_element(By.LINK_TEXT, "próximo")
        page.click()
    
    
    for i in range(len(listsize)):
        try:
            element = driver.find_element(By.CSS_SELECTOR, "div[class = 'resultado']")
            lista = element.find_elements(By.TAG_NAME, "li")
            link = lista[i].find_element(By.TAG_NAME, "a")
            link.click()

            WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a#idbtnabrircurriculo.button"))
            )

            curriculo = driver.find_element(By.PARTIAL_LINK_TEXT, value = "Abrir Currículo")
            time.sleep(4)
            curriculo.click()

            wait.until(EC.number_of_windows_to_be(2))

            handles = []
            handles = driver.window_handles
            newhandle = handles[1]
            driver.switch_to.window(newhandle)

            nome = driver.find_element(By.CLASS_NAME, "nome").text
            ul = driver.find_elements(By.TAG_NAME, "li")
            string = ul[1].text
            idlattes = re.findall(r'\d+', string)
            idlattes = idlattes[0]

            perfis += 1
            print(f'******\nO número de perfis vizualisados foi de: {perfis}\n*****')
            dictionary.update({nome: idlattes})
            print(dictionary)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            close = driver.find_element(By.ID, "idbtnfechar")
            close.click()
            
        except Exception as e:
            print(e)
    
    traffic += 1
    try:
        page = driver.find_element(By.LINK_TEXT, str(traffic))
        el = driver.find_element(By.CSS_SELECTOR, "div[class = 'resultado']")
        listsize = el.find_elements(By.TAG_NAME, "li")
        page.click()
        time.sleep(3)
    except:
        pass
            
print(dictionary)

time.sleep(10)

driver.quit()