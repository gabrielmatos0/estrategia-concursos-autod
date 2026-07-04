from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from driver import Driver
from time import sleep
import requests
from pathlib import Path
import os

DOWNLOAD_DIR = os.path.join(Path(__file__).parent, 'downloads')

def get_nome_curso(driver:Driver):
    return driver.esperar_elemento(By.CSS_SELECTOR, 'h2.CourseInfo-content-title').text


def get_nome_aula(web_element):
    return web_element.find_element(By.CSS_SELECTOR, 'h2.SectionTitle').text


def get_tipo_pdf(web_element) -> str:
    return web_element.find_element(By.CSS_SELECTOR, '.LessonButton-text>span').text


def get_nome_video(web_element):
    nome =  ' - '.join(web_element.text.split('\n'))
    nome = nome.replace('<', '') if '<' in nome else nome
    nome = nome.replace('>', '') if '>' in nome else nome
    nome = nome.replace(':', '') if ':' in nome else nome
    nome = nome.replace('"', '') if '"' in nome else nome
    nome = nome.replace("'", '') if "'" in nome else nome
    nome = nome.replace("/", '') if "/" in nome else nome
    nome = nome.replace("\\", '') if "\\" in nome else nome
    nome = nome.replace("|", '') if "|" in nome else nome
    nome = nome.replace("?", '') if "?" in nome else nome
    nome = nome.replace("*", '') if "*" in nome else nome
    return nome


def ignorar_pesquisa(driver):
    pass


def req_download(url:str, file_name:str):
    try:
        response = requests.get(url)

        with open(file_name, 'wb') as file:
            file.write(response.content)
        return True
    except:
        return False
    

def get_pdfs(driver:Driver, last_class, NOME_CURSO, NOME_AULA):

    btns = driver.esperar_elementos(By.CLASS_NAME, 'LessonButton')

    ### BAIXAR PDFs DA AULA
    for i, btn in enumerate(btns):
        if not 'Baixar Livro Eletrônico'.lower().strip() in btn.text.lower().strip():
            continue

        TIPO_PDF = get_tipo_pdf(btn)
        TIPO_PDF = TIPO_PDF.split()[-1]
        pdf_name = os.path.join(DOWNLOAD_DIR, f'{NOME_CURSO}_{NOME_AULA}_PDF_{TIPO_PDF}.pdf')

        pdf_url = btn.get_attribute('href')

        if req_download(pdf_url, pdf_name):
            print('PDF baixado!')
            continue
        print('erro ao baixar PDF...')
        continue

        ### se a jnela de avaliação do curso aparecer novamente, finalizar a função "ignorar_pesquisa()"
        ### 1. devo clicar em "ignorar pesquisa" e no ícore para fechar ( X )
        # if last_class:
        #     sleep(1)
        #     driver.esperar_elemento_aparecer(By.CLASS_NAME, 'icon-close').click()
        #     sleep(1)
        #     btn.click()

            # btns2 = driver.esperar_elementos(By.CLASS_NAME, 'LessonButton')
            # print(btns2[i] == btn)
            # btns2[i].click()
        ###


def get_videos(driver:Driver, NOME_CURSO, NOME_AULA, video_resolution="480p"):
    ### BAIXAR VIDEOS
    videos = driver.esperar_elementos(By.CLASS_NAME, 'VideoItem')

    for i, video in enumerate(videos):
        NOME_VIDEO = get_nome_video(video)
        driver.focar_janela(web_element=video)
        sleep(2)

        ### procurar elemento com "Opções de Download"
        if i == 0:
            elements = driver.esperar_elementos(By.CLASS_NAME, 'Collapse-header-container')

            for ele in elements:
                text = ele.text.strip()
                if 'Opções de download' in text:
                    # ele.find_element(By.CLASS_NAME, 'Collapse-header-arrow ').click()
                    driver.focar_janela(web_element=ele)
                    # ele.click()
                    ####
                    break

        ### procurar elementos de resolução de vídeo
        sleep(1)
        btns = driver.esperar_elementos(By.CSS_SELECTOR, '.Button.-small')
        sleep(1)

        for btn in btns:
            btn_text = btn.text.lower().strip()

            if video_resolution not in btn_text:
                continue

            video_name = os.path.join(DOWNLOAD_DIR, f'{NOME_CURSO}_{NOME_AULA}_VD-{video_resolution}_{NOME_VIDEO}.mp4')
            url_video = btn.get_attribute('href')

            if req_download(url_video, video_name):
                print('Vídeo baixado!', NOME_VIDEO)
            else:
                print('Erro ao baixar vídeo:', NOME_VIDEO)

            break


def login(driver:Driver, email:str, password:str):
    email_input = driver.esperar_elemento_aparecer(By.NAME, 'loginField')

    if not email_input:
        return

    email_input.send_keys(email)
    sleep(.5)
    driver.driver_actions.send_keys(Keys.TAB).send_keys(password).perform()

    driver.esperar_elemento(By.CSS_SELECTOR, 'button.ui-w-full').click()



def main(url_aula:str, email, password):
    if not os.path.exists(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    driver = Driver('EstrategiaConcursos')
    driver.get(url_aula)
    driver.driver.maximize_window()
    login(driver, email, password)
    NOME_CURSO = get_nome_curso(driver)
    class_list = driver.esperar_elementos(By.CLASS_NAME, 'LessonList-item')


    last_class = False
    for i, class_div in enumerate(class_list):
        NOME_AULA = get_nome_aula(class_div)
        print(NOME_AULA)

        if i == len(class_list) - 1:
            last_class = True

        driver.focar_janela(web_element=class_div)
        get_pdfs(driver, last_class, NOME_CURSO, NOME_AULA)
        get_videos(driver, NOME_CURSO, NOME_AULA, '480p')
        sleep(1)

if __name__ == '__main__':
    print(DOWNLOAD_DIR)