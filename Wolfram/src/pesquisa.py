from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class Arq:
    def __init__(self, nome, dir=None):
        if dir is not None:
            self.dir = dir

        else:
            self.dir = os.path.dirname(os.path.realpath(__file__))

        self.nome = nome
        self.local = os.path.join(self.dir, self.nome)

    def testar(self):
        if os.path.isfile(self.local):
            return True

        else:
            return False

    def gerar_arq(self):
        if self.testar():
            self.arq = open(self.local, "r")

        else:
            print("arquivo não existe")

    def localizar_chave(self, chave: str) -> str:
        for linha in self.arq:
            conteudo = linha[:-1].split("=")
            if conteudo[0] == chave:
                return conteudo[1]


class Driver:
    def __init__(self, path):
        self.path = path
        self.driver = webdriver.Chrome(self.path)
        self.elementos = {}

    def abrir(self, link):
        self.driver.get(link)

    def gerar_elemento(self, classe: str, nome: str, delay: int = 0):
        if delay == 0:
            self.elementos[nome] = self.driver.find_element_by_class_name(
                classe)

        else:
            elemento = WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, classe)))
            self.elementos[nome] = elemento

    def esperar(self, t: int):
        self.driver.implicitly_wait(10)

    def getElemento(self, nome: str):
        return self.elementos[nome]

    def escrever(self, nome: str, palavra: str):
        self.getElemento(nome).send_keys(palavra)

    def escrever_enter(self, nome: str):
        self.getElemento(nome).send_keys(Keys.RETURN)

    def ler_atributo(self, nome: str, atributo: str) -> str:
        return self.getElemento(nome).get_attribute(atributo)

    def quit(self):
        self.driver.quit()
