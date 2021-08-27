import interface
import implementar_pesquisa


def pesquisar(**kwargs):
    if "janela" in kwargs.keys():
        janela = kwargs["janela"]
        problema = ""
        for input in janela.inputs:
            if input.nome == "pes":
                problema = input.input

        conteudo = implementar_pesquisa.main(problema)
        setartextovar(conteudo, janela)


def setartextovar(conteudo, janela):
    text_res = interface.Texto(10, 200, 30, conteudo, "res")
    janela.addTextos([text_res])


def setarbots(janela: interface.Janela):
    bot_go = interface.Botao(10, 90, 0, 0, "go", "go", 30,
                             [120, 120, 120], pesquisar, {"janela": janela})
    janela.addBotões([bot_go])


def setartextos(janela: interface.Janela):
    text_pes = interface.Texto(
        10, 10, 30, "conta a ser pesquisada:", "pesquisa")
    janela.addTextos([text_pes])


def setarinputs(janela: interface.Janela):
    inpu_pes = interface.Inp(10, 50, 10, 30, "", "pes")
    janela.addInputs([inpu_pes])


def main():
    janela = interface.Janela(600, 400, "wolfram")
    setarbots(janela)
    setartextos(janela)
    setarinputs(janela)
    janela.iniciar()
    janela.main_loop()


if __name__ == "__main__":
    main()
