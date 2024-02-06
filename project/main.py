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
input_element.send_keys('(oncológicos OR oncology OR anticâncer OR anticancer OR antineoplásicos OR antineoplastic OR anticancerígeno OR anticancer OR antineoplásicas OR antitumoral OR antitumor OR quimioterápicos OR chemotherapy OR tumor OR neoplasm OR neoplasia) AND (câncer OR cancer OR neoplasm OR Leukemia OR Carcinoma OR Astrocytoma OR Astrocitoma OR Sarcoma OR Lymphoma or Linfoma OR cholangiocarcinoma or Colangiocarcinoma OR osteosarcoma or Osteossarcoma OR Histiocytoma OR fibro-histiocitoma OR ependymoma OR Ependimoma OR Medulloblastoma OR Meduloblastoma OR blastoma OR Hodgkin OR Non-Hodgkin OR Chordoma OR Cordoma OR adenocarcinoma OR Esthesioneuroblastoma OR Estesioneuroblastoma OR neuroblastoma OR Retinoblastoma OR melanoma OR mesothelioma OR esotelioma OR rhabdomyosarcoma OR rabdomiosarcoma OR glioblastoma)')

bolsproducnpqbutton = driver.find_element(By.CSS_SELECTOR, "input#filtro0")
bolsproducnpqbutton.click()

cnpq1button = driver.find_element(By.CSS_SELECTOR, "input#checkbox1A")
cnpq1button.click()
cnpq2button = driver.find_element(By.CSS_SELECTOR, "input#checkbox1B")
cnpq2button.click()
cnpq3button = driver.find_element(By.CSS_SELECTOR, "input#checkbox1C")
cnpq3button.click()
cnpq4button = driver.find_element(By.CSS_SELECTOR, "input#checkbox1D")
cnpq4button.click()
cnpq5button = driver.find_element(By.CSS_SELECTOR, "input#checkbox2")
cnpq5button.click()
aplicarcnpqbutton = driver.find_element(By.CSS_SELECTOR, "a#preencheCategoriaNivelBolsa.button")
aplicarcnpqbutton.click()

gruposdepesquisabutton = driver.find_element(By.CSS_SELECTOR, "input#filtro9")
gruposdepesquisabutton.click()
filtrobutton = driver.find_element(By.CSS_SELECTOR, "input#participaDGP")
filtrobutton.click()
time.sleep(7)#aqui você aperta o botao!

atuacaoprofissionalbutton = driver.find_element(By.CSS_SELECTOR, "input#filtro4")
atuacaoprofissionalbutton.click()

selectprofissao = driver.find_element(By.CSS_SELECTOR, "select#codigoGrandeAreaAtuacao.input-text")
select = Select(selectprofissao)
select.select_by_value('40000001')
time.sleep(2)

selectarea = driver.find_element(By.CSS_SELECTOR, "select#codigoAreaAtuacao.input-text")
select = Select(selectarea)
select.select_by_value('40100006')
time.sleep(7)#aqui você aperta o botao!

botaopesquisa = driver.find_element(By.CSS_SELECTOR, "a#botaoBuscaFiltros.button")
botaopesquisa.click()

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
traffic = 2
for j in range(numero):
    if traffic % 10 == 0:
        page = driver.find_element(By.LINK_TEXT, "próximo")
    else:
        page = driver.find_element(By.LINK_TEXT, str(traffic))
        el = driver.find_element(By.CSS_SELECTOR, "div[class = 'resultado']")
        listsize = el.find_elements(By.TAG_NAME, "li")
    
    
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
            print(f'O número de perfis vizualisados foi de: {perfis}')
            dictionary.update({nome: idlattes})
            print(dictionary)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            close = driver.find_element(By.ID, "idbtnfechar")
            close.click()
            
        except Exception as e:
            print(e)
    
    page.click()
    time.sleep(3)
    traffic += 1
            
print(dictionary)

time.sleep(10)

driver.quit()