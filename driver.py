from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from time import sleep
from functions import get_chrome_profile_path

class Driver:
    def __init__(self, profile_name, wait_time=15):
        custom_profile = get_chrome_profile_path(profile_name)

        options = Options()
        # options.add_experimental_option("prefs", prefs)
        options.add_argument(f"--user-data-dir={custom_profile}")
        options.add_argument(f"--profile-directory={profile_name}") 

        service = Service(ChromeDriverManager().install())
        self._driver = Chrome(service=service, options=options)
        self.driver_wait = WebDriverWait(self._driver, wait_time)
        self.driver_actions = ActionChains(self._driver)


    def get(self, url):
        self._driver.get(url)


    def elemento_presente(self, by, valor, wait=None):
        if not wait:
            wait = self.driver_wait

        return wait.until(EC.presence_of_element_located((by, valor)))


    def elemento_visivel(self, by, valor, wait=None):
        if not wait:
            wait = self.driver_wait

        return wait.until(EC.visibility_of_element_located((by, valor)))


    def elemento_clicavel(self, by, valor, wait=None):
        if not wait:
            wait = self.driver_wait

        return wait.until(EC.element_to_be_clickable((by, valor)))


    def esperar_elemento(self, by, valor, wait=None):
        self.elemento_presente(by, valor, wait)
        self.elemento_visivel(by, valor, wait)
        return self.elemento_clicavel(by, valor, wait)
    
    
    def esperar_elementos(self, by, valor):
        self.driver_wait.until(EC.presence_of_all_elements_located((by, valor)))
        return self.driver_wait.until(EC.visibility_of_all_elements_located((by, valor)))


    def preencher_campo(self, by, valor_by, valor_campo):
        self.esperar_elemento(by, valor_by).clear()
        self.esperar_elemento(by, valor_by).send_keys(valor_campo)


    def preencher_formulario(self, campos:list, by_btn_enviar, btn_enviar):
        sleep(2)
        for campo in campos:
            by = campo['by']
            valor_by = campo['valor_by']
            valor_campo = campo['valor_campo']

            self.preencher_campo(by, valor_by, valor_campo)
            self._driver.find_element(by, valor_by).clear()
            self._driver.find_element(by, valor_by).send_keys(valor_campo)
        
        self.focar_janela(by_btn_enviar, btn_enviar)
        # self.esperar_elemento(by_btn_enviar, btn_enviar).click()


    def focar_janela_simples(self, by_janela=None, valor_janela=None):
        elemento_janela = self.esperar_elemento(by_janela, valor_janela)
        self.driver_actions.move_to_element(elemento_janela).click().perform()


    def focar_janela(self, by_janela=None, valor_janela=None, web_element=None, element_to_click=None): 
        if not web_element:
            elemento_janela = self.esperar_elemento(by_janela, valor_janela)
            if not element_to_click:
                element_to_click = elemento_janela

            self.driver_actions.move_to_element(elemento_janela).click(element_to_click).perform()

            return elemento_janela
        else:
            if not element_to_click:
                element_to_click = web_element
            self.driver_actions.move_to_element(web_element).click(element_to_click).perform()
            return web_element


    def fechar_janela(self, by_janela, valor_janela, by_fechar, valor_fechar):
        self.focar_janela(by_janela, valor_janela)

        self.esperar_elemento(by_fechar, valor_fechar).click()
    

    def esperar_elemento_sumir(self, by, valor):
        wait = WebDriverWait(self._driver, 3)
        try:
            while wait.until(EC.visibility_of_element_located((by, valor))):
                sleep(3)
        except:
            return


    def esperar_elemento_aparecer(self, by, valor):
        wait = WebDriverWait(self._driver, 3)
        c = 0
        while c != 3:
            try:
                elemento = self.esperar_elemento(by, valor, wait)
                return elemento
            except TimeoutException:
                c += 1
                continue


    @property
    def driver(self):
        return self._driver


if __name__ == '__main__':
    pass
