import pygame

pygame.init()
pygame.font.init()


class Janela:
    def __init__(self, w: int, h: int, nome: str):
        self.w = w
        self.h = h
        self.nome = nome
        self.botoes = []
        self.textos = []
        self.inputs = []
        self.inpu = None

    def iniciar(self):
        self.disp = pygame.display
        self.disp.set_caption(self.nome)
        self.screen = self.disp.set_mode((self.w, self.h))
        self.fonte = pygame.font.SysFont('arial', 25)

    def addBotões(self, bots: list):
        for bot in bots:
            self.botoes.append(bot)

    def addTextos(self, textos: list):
        for texto in textos:
            self.textos.append(texto)

    def substTexto(self, texto):
        for i, t in enumerate(self.textos):
            if t.nome == texto.nome:
                self.textos[i] = texto

    def addInputs(self, inputs: list):
        for inpu in inputs:
            self.inputs.append(inpu)

    def click(self, pos):
        for bot in self.botoes:
            limite_x = (pos[0] >= bot.campo_min[0]
                        and pos[0] <= bot.campo_max[0])
            limite_y = (pos[1] >= bot.campo_min[1]
                        and pos[1] <= bot.campo_max[1])
            if limite_x and limite_y:
                retorno = bot.click()
                if retorno is not None:
                    self.texto = retorno

                break

        for inpu in self.inputs:
            limite_x = (pos[0] >= inpu.campo_min[0]
                        and pos[0] <= inpu.campo_max[0])
            limite_y = (pos[1] >= inpu.campo_min[1]
                        and pos[1] <= inpu.campo_max[1])
            if limite_x and limite_y:
                self.inpu = inpu
                break

        else:
            self.inpu = None

    def atualizar_janela(self):
        self.screen.fill((200, 200, 200))
        for texto in self.textos:
            conteudo = texto.printar()
            for frase, posx, posy in conteudo:
                self.screen.blit(frase, (posx, posy))

        for bot in self.botoes:
            pygame.draw.rect(self.screen, bot.cor, [
                             bot.x, bot.y, bot.w, bot.h])
            texto = bot.fonte.render(bot.conteudo, False, (10, 10, 10))
            self.screen.blit(texto, (bot.x + 5, bot.y))

        for inpu in self.inputs:
            for i in range(inpu.maximo):
                letra = ""
                if i < len(inpu.amostra):
                    letra = inpu.amostra[i]

                inpu.gerar_amostra()
                pygame.draw.rect(self.screen, inpu.cor, [
                                 inpu.x + inpu.w * i, inpu.y, inpu.w, inpu.h])
                texto = inpu.fonte.render(letra, False, (10, 10, 10))
                self.screen.blit(texto, (inpu.x + inpu.w * i, inpu.y))

        if self.inpu is not None:
            for i, letra in enumerate(self.inpu.input):
                local_escolhido = self.inpu.x + 5 + \
                    self.inpu.fonte.size(
                        self.inpu.amostra[:self.inpu.cursor])[0]
                local_escolhido = self.inpu.x + inpu.w * self.inpu.cursor - 1
                pygame.draw.rect(self.screen, [10, 10, 10], [
                                 local_escolhido, inpu.y, 1, inpu.h - 5])

        pygame.display.flip()

    def main_loop(self):
        run = True
        while run:
            self.atualizar_janela()
            # if str(list(pygame.key.get_pressed())[42]) == "1":
            #     if self.inpu != None:
            #         self.inpu.input = self.inpu.input[:-1]
            #         pygame.time.wait(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.click(pos)

                elif event.type == pygame.KEYDOWN:
                    numeros = "0123456789"
                    letras_min = "abcdefghijklmnopqrstuvwxyz"
                    letras_mai = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    especiais = "+-=*/()"
                    opções = numeros + letras_min + letras_mai + especiais
                    if self.inpu is not None:
                        indice = self.inpu.cursor + self.inpu.indice_am

                    else:
                        indice = 0

                    if event.unicode in opções and event.unicode != "":
                        if self.inpu is not None:
                            self.inpu.input = self.inpu.input[:indice] + \
                                event.unicode + self.inpu.input[indice:]
                            self.inpu.cursor += 1

                    elif str(event.key) == "32":
                        if self.inpu is not None:
                            self.inpu.input = self.inpu.input[:indice] + \
                                " " + self.inpu.input[indice:]
                            self.inpu.cursor = min(
                                self.inpu.cursor + 1, len(self.inpu.amostra))

                    elif str(event.key) == "8":
                        if self.inpu is not None:
                            fatia_ante = self.inpu.input[:indice - 1]
                            fatia_pos = self.inpu.input[indice:]
                            self.inpu.input = fatia_ante + fatia_pos
                            self.inpu.cursor = max(0, self.inpu.cursor - 1)

                    elif str(event.key) == "1073741904":
                        if self.inpu is not None:
                            self.inpu.cursor = self.inpu.cursor - 1
                            self.inpu.gerar_amostra()

                    elif str(event.key) == "1073741903":
                        if self.inpu is not None:
                            self.inpu.cursor = self.inpu.cursor + 1
                            self.inpu.gerar_amostra()

                    elif str(event.key) == "13":
                        pass


class Botao:
    def __init__(self, x: int, y: int, w: int, h: int, conteudo: str,
                 nome: str, tamanho: int, cor: list, func, inputs: dict = {}):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.conteudo = conteudo
        self.nome = nome
        self.tamanho = tamanho
        self.cor = cor
        self.func = func
        self.inputs = inputs
        self.retorno = ""
        self.fonte = pygame.font.Font(pygame.font.get_default_font(), tamanho)
        self.formatar()
        self.campo_min = [self.x, self.y]
        self.campo_max = [self.x + self.w, self.y + self.h]

    def formatar(self):
        if self.h == 0:
            self.h = self.fonte.size(self.conteudo)[1]

        if self.w == 0:
            self.w = self.fonte.size(self.conteudo)[0] + 10

    def click(self):
        self.retorno = self.func(**self.inputs)


class Texto:
    def __init__(self, x: int, y: int, tamanho: int, conteudo: str, nome: str):
        self.x = x
        self.y = y
        self.tamanho = tamanho
        self.conteudo = conteudo
        self.nome = nome
        self.fonte = pygame.font.Font(pygame.font.get_default_font(), tamanho)

    def printar(self) -> list:
        lista = []
        y = self.y
        for texto in self.conteudo.split("\n"):
            textsurface = self.fonte.render(texto, False, (10, 10, 10))
            lista.append([textsurface, 10, y])
            y += self.tamanho

        return lista


class Inp:
    def __init__(self, x: int, y: int, maximo: int, tamanho: int,
                 input: str = "", nome: str = ""):
        self.tamanho = tamanho
        self.fonte = pygame.font.Font(
            pygame.font.get_default_font(), self.tamanho)
        self.x = x
        self.y = y
        self.maximo = maximo
        self.w = self.fonte.size("w")[0] + 1
        self.h = self.fonte.size("w")[1]
        self.cor = [245, 245, 245]
        self.input = input
        self.nome = nome
        self.cursor = 0
        self.indice_am = 0
        self.amostra = self.input
        self.campo_min = [self.x, self.y]
        self.campo_max = [self.x + self.w * self.maximo, self.y + self.h]

    def gerar_amostra(self):
        self.amostra = self.input[self.indice_am:]
        if self.cursor < 0 and self.indice_am > 0:
            self.indice_am += -1
            maximo = min(self.indice_am + self.maximo,
                         len(self.input) - self.indice_am)
            self.amostra = self.input[self.indice_am:maximo]
            self.cursor += 1

        elif self.cursor > self.maximo:
            self.cursor += -1
            final = self.indice_am + self.maximo
            if final <= len(self.input):
                self.indice_am += 1
                self.amostra = self.input[self.indice_am:final]

        if len(self.amostra) > self.maximo:
            if self.cursor < self.maximo:
                self.amostra = self.amostra[:-1]

            elif self.cursor == self.maximo:
                self.amostra = self.amostra[1:]
