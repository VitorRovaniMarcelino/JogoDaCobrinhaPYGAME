# imports:
import pygame
from pygame.locals import *
from sys import exit
from random import randint

# inicializador:
pygame.init()
pygame.mixer.init()

icone = pygame.image.load('imagens/icone.png')
pygame.display.set_icon(icone)

# música de fundo:
lista_musicas = [
'audios/Cartoon, Jéja - On & On.mp3',
'audios/Desmeon - Hellcat .mp3',
'audios/Janji - Heroes Tonight.mp3',
'audios/Warriyo - Mortals.mp3',
'audios/DEAF KEV - Invincible.mp3',
'audios/Cartoon, Jéja - Why We Lose.mp3',
'audios/Electro-Light - Symbolism.mp3',
'audios/Different Heaven My Heart.mp3',
'audios/Syn Cole - Feel Good.mp3',
'audios/Jo Cohen & Sex Whales - We Are.mp3',
'audios/Different Heaven - Nekozilla _ Electro.mp3']
musica_atual = 0
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load(lista_musicas[musica_atual])
pygame.mixer.music.play(-1) 

# som que faz quando encosta um objeto no outro
som_tocar = pygame.mixer.Sound("audios/somtocar.mp3")
som_tocar.set_volume(0.5)

# som ao morrer
som_morrer = pygame.mixer.Sound("audios/sommorrer.mp3")
som_morrer.set_volume(0.5)

# tamanho da tela:
largura = 640
altura = 480

# tamanho de um objeto:
largura_cobra = 25
altura_cobra = 25

# posicao do objeto na tela:
x_cobra = int(largura / 2)
y_cobra = int(altura / 2)

# velocidade da cobra
velocidade_cobra = 20
x_controle = velocidade_cobra
y_controle = 0

listaCobra = []

def gerar_comida_fora_da_cobra(lista_cobra):
    while True:
        x = randint(0, (largura - 40) // 40) * 40
        y = randint(0, (altura - 40) // 40) * 40
        if [x, y] not in lista_cobra:
            return x, y

# posicao de outro objeto na tela:
x_comida, y_comida = gerar_comida_fora_da_cobra(listaCobra)

# fazer um texto na tela
fonte_texto = pygame.font.SysFont('comicsans', 30, True, False)
fonte_musica = pygame.font.SysFont('comicsans', 20, True, False)
quantidade_pontos = 0

# atribuindo o tamanho da tela
tela = pygame.display.set_mode((largura, altura))

# escrevendo o nome da tela
pygame.display.set_caption("Jogo da Cobrinha")

# atribuindo a quantidade de frames do jogo
frames = pygame.time.Clock()

# Carregar as imagens para cada direção
imagem_cima = pygame.image.load("imagens/cobra_cima.png").convert_alpha()
imagem_baixo = pygame.image.load("imagens/cobra_baixo.png").convert_alpha()
imagem_esquerda = pygame.image.load("imagens/cobra_esquerda.png").convert_alpha()
imagem_direita = pygame.image.load("imagens/cobra_direita.png").convert_alpha()

corpo_vertical = pygame.image.load("imagens/corpoCobra.png").convert_alpha()
corpo_horizontal = pygame.image.load("imagens/corpoCobra.png").convert_alpha()

imagem_comida = pygame.image.load("imagens/comida.png").convert_alpha()
imagem_comida = pygame.transform.scale(imagem_comida, (30, 30))
corpo = corpo_vertical
imagem_atual = imagem_direita

# imagem do fundo
imagem_fundo = pygame.image.load("imagens/imagemFundo.png").convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

morreu = False

def aumentaCobra(listaCobra):
    for i, posicao in enumerate(listaCobra):
        if i == len(listaCobra) - 1:
            tela.blit(imagem_atual, (posicao[0], posicao[1]))
        else:
            tela.blit(corpo, (posicao[0], posicao[1]))

def reiniciar_jogo():
    global quantidade_pontos, comprimentoInicial, x_cobra, y_cobra, x_controle, y_controle, listaCobra, x_comida, y_comida, morreu, musica_atual, imagem_atual
    quantidade_pontos = 0
    comprimentoInicial = 5
    x_cobra = int(largura / 2)
    y_cobra = int(altura / 2)
    x_controle = velocidade_cobra
    y_controle = 0
    listaCobra = []
    x_comida, y_comida = gerar_comida_fora_da_cobra(listaCobra)
    morreu = False
    imagem_atual = imagem_direita

comprimentoInicial = 5

while True:
    frames.tick(20)
    tela.blit(imagem_fundo, (0,0))
    
    mensagem_pontos = f"Pontos: {quantidade_pontos}"
    texto_pontos = fonte_texto.render(mensagem_pontos, True, (255, 255, 255))
    
    nome_musica = lista_musicas[musica_atual].split('/')[-1]
    musica = f"Música atual:"
    texto_musica = fonte_musica.render(musica, True, (255, 255, 255))
    musica_tocando = nome_musica
    musicaTocando = fonte_musica.render(musica_tocando, True, (255, 255, 255))
    mensagem_musica  = "Pressione 'N' para Avançar a música e 'P' para Voltar."
    mudar_musica = fonte_musica.render(mensagem_musica, True, (255, 255, 255))

    direcao_trocada = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
            
        if event.type == KEYDOWN:
            if event.key == K_n:
                musica_atual = (musica_atual + 1) % len(lista_musicas)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(lista_musicas[musica_atual])
                pygame.mixer.music.play(-1)
            elif event.key == K_p:
                musica_atual = (musica_atual - 1 + len(lista_musicas)) % len(lista_musicas)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(lista_musicas[musica_atual])
                pygame.mixer.music.play(-1)

            if not direcao_trocada:
                if event.key == K_w and y_controle == 0:
                    y_controle = -velocidade_cobra
                    x_controle = 0
                    imagem_atual = imagem_cima
                    corpo = corpo_horizontal
                    direcao_trocada = True
                elif event.key == K_a and x_controle == 0:
                    x_controle = -velocidade_cobra
                    y_controle = 0
                    imagem_atual = imagem_esquerda
                    corpo = corpo_vertical
                    direcao_trocada = True
                elif event.key == K_s and y_controle == 0:
                    y_controle = velocidade_cobra
                    x_controle = 0
                    imagem_atual = imagem_baixo
                    corpo = corpo_horizontal
                    direcao_trocada = True
                elif event.key == K_d and x_controle == 0:
                    x_controle = velocidade_cobra
                    y_controle = 0
                    imagem_atual = imagem_direita
                    corpo = corpo_vertical
                    direcao_trocada = True

    x_cobra += x_controle
    y_cobra += y_controle

    cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, largura_cobra, altura_cobra))
    comida = tela.blit(imagem_comida, (x_comida, y_comida))

    if x_cobra >= largura:
        x_cobra = 0
    elif x_cobra < 0:
        x_cobra = largura - largura_cobra

    if y_cobra >= altura:
        y_cobra = 0
    elif y_cobra < 0:
        y_cobra = altura - altura_cobra

    if cobra.colliderect(comida):
        som_tocar.play()
        quantidade_pontos += 1
        x_comida, y_comida = gerar_comida_fora_da_cobra(listaCobra)
        comprimentoInicial += 1

    listaCabeca = [x_cobra, y_cobra]
    listaCobra.append(listaCabeca)

    if(listaCobra.count(listaCabeca) > 1):
        fonte2 = pygame.font.SysFont('rockwellnegrito', 20, True, False)
        mensagem_perdeu = 'Perdeu! Tecla R para reiniciar.'
        texto_perdeu = fonte2.render(mensagem_perdeu, True, (255, 255, 255))
        retanguloTexto = texto_perdeu.get_rect()

        mensagem_pontos_perdeu = f'Quantidade de pontos: {quantidade_pontos}'
        texto_pontos_perdeu = fonte2.render(mensagem_pontos_perdeu, True, (255, 255, 255))
        retanguloTexto2 = texto_pontos_perdeu.get_rect()
        
        morreu = True
        som_morrer.play()
        
        while morreu:
            tela.blit(imagem_fundo, (0,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
            
            retanguloTexto.center = (largura//2, altura//2)
            retanguloTexto2.center = (largura//2, (altura//2) + 30)

            fundo_texto = pygame.Rect(retanguloTexto.left - 10, retanguloTexto.top - 10, retanguloTexto.width + 20, retanguloTexto.height + 20)
            fundo_texto2 = pygame.Rect(retanguloTexto2.left - 10, retanguloTexto2.top - 10, retanguloTexto2.width + 20, retanguloTexto2.height + 20)

            pygame.draw.rect(tela, (255, 0, 0), fundo_texto)
            pygame.draw.rect(tela, (255, 0, 0), fundo_texto2)
            
            tela.blit(texto_perdeu, retanguloTexto)
            tela.blit(texto_pontos_perdeu, retanguloTexto2)
            
            pygame.display.update()

    if len(listaCobra) > comprimentoInicial:
        del listaCobra[0]

    aumentaCobra(listaCobra)

    tela.blit(texto_pontos, (480, 20))
    tela.blit(texto_musica, (20, 20))
    tela.blit(musicaTocando, (20, 50))
    tela.blit(mudar_musica, (10, 440))

    pygame.display.update()