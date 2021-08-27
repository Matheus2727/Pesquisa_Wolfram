import pesquisa


def main(problema):
    arq = pesquisa.Arq("infos.txt")
    arq.gerar_arq()
    local_driver = arq.localizar_chave("path")
    link = arq.localizar_chave("link")
    driver = pesquisa.Driver(local_driver)
    driver.abrir(link)
    driver.gerar_elemento("_2oXzi", "search", 10)
    driver.escrever("search", problema)
    driver.escrever_enter("search")
    driver.gerar_elemento("_3vyrn", "resultado", 10)
    resultado = driver.ler_atributo("resultado", "alt")
    return resultado


if __name__ == "__main__":
    main()
