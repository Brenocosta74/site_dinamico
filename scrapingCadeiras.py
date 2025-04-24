# pip install selenium

# módulo para controlar o navegador
from selenium import webdriver

# localizador de elementos 
from selenium.webdriver.common.by import By

# serviço para configurar o caminho do exxecutável chromedriver
from selenium.webdriver.chrome.service import Service

# classe que permite executar ações avançadas(o mover do mouse, clique/arrasta, etc)
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera de forma explícita até que uma condição seja satisfeita(ex: que um elemento apareça)
from selenium.webdriver.support.ui import WebDriverWait

# condições esperadas usadas com o WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# trabalhar com dataframe
import pandas as pd

# uso de funções relacionadas ao tempo
import time

# uso de tratamenot de exceção
from selenium.common.exceptions import TimeoutException

# caminho do ChromeDriver (altere para seu local)
caminho_driver = r"c:\Program Files\chromedriver-win64\chromedriver.exe"

# configuração ao WebDriver
service = Service(caminho_driver) #navegador controlado pelo Selenium
options = webdriver.ChromeOptions() # configura opções do navegador
options.add_argument("--disable-gpu") # evita possíveis erros gráficos
options.add_argument("--window-size=1920,1080") # define uma resolução fixa

# incialização ao WebDriver
driver = webdriver.Chrome(service=service, options=options) # inicialização do navegador

# URl inicial
url_base = "https://www.kabum.com.br/espaco-gamer/cadeiras-gamer"
driver.get(url_base)
time.sleep(3) # aguarda 5 segundos para garantir que a pág carregue

#criar um dicionário vazio para armazenar as marcas para armazenar as marcas e preços das cadeiras
dic_produtos = {"marca": [], "preco": []}

# vamos ininciar na página 1 e incrementos a cada troca de página
pagina = 1

while True:
    print(f"\n Coletando dados da página {pagina}...")

    try:



    #WebDriverWait(driver,10): cria uma espera de até 10 segundos
    #until(...): faz com que o código espere até que a condição seja verdadeira
    #ec.presence_of_all_elements_located(..) verifica se todos os elementos "productCard" estão acessíveis
    #By.CLASS_NAME, "productCard": indica que a busca será feita através da classe css
        WebDriverWait(driver,10).until(
            ec.presence_of_element_located((By.CLASS_NAME, "productCard"))
        )
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        print("Tempo de espera execido!")

    produtos = driver.find_elements(By.CLASS_NAME, "productCard")

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()

            print(f"{nome} - {preco}")

            dic_produtos["marca"].append(nome)
            dic_produtos["preco"].append(preco)

        except Exception:
            print("Erro ao coletar dados:", Exception)

# Encontar botão da próxima página
    try:
        botao_proximo = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )
        if botao_proximo:
            driver.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(1)

            # Clicar no botão
            driver.execute_script("arguments[0].click();", botao_proximo)
            print(f"Indo para a pagina {pagina}")
            pagina += 1

            time.sleep(1)

        else:
            print("Você chegou na ultima página")
            break
    
    except Exception as e:
        print("Erro ao tentar avançar para a próxima página")
        break


# Fechar o navegador
driver.quit()

# DataFrame
df = pd.DataFrame(dic_produtos)

# Salvar os dados em excel
df.to_excel("cadeiras.xlsx", index= False)

print(f"Arquivo 'cadeiras' salvo com sucesso! {len(df)} produtos capturados")