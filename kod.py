import pygame
import sys
import os
import random
pygame.mixer.init()
MODRA = (0,0,255)
CERVENA = (255,0,0)
BULL_SPEED=10
posuv = 8
xyellow = 300
yyellow = 100
xred = 700
yred = 300
pygame.init()
WIDTH = 900
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space ships")
BIELA = (255,255,255)
CIERNA = (0,0,0)
FPS = 60
run = True
clock = pygame.time.Clock()
red = pygame.image.load("spaceship_red.png")
yellow = pygame.image.load("spaceship_yellow.png")
space = pygame.image.load("space.png")
ZIVOT_PRAVEHO  = 10
ZIVOT_LAVEHO = 10
yellow_bullets = []
red_bullets = []
MAX_BULLETS = 3
ZVUK = pygame.mixer.Sound("zvuk.wav")
ZVUK.play()
ZVUK2 = pygame.mixer.Sound("zvuk2 (2).wav")


def draw_window():
    screen.blit(space,(0,0))
    pygame.draw.rect(screen,CIERNA,(WIDTH//2-5,0,10,HEIGHT))
    screen.blit(yellow,(xred,yred))
    screen.blit(red,(xyellow,yyellow))



def pohyb_zlteho(keys_pressed):
    global xyellow
    global yyellow
    if keys_pressed[pygame.K_a]:
        if xyellow - posuv >= 0:
            xyellow -= posuv
    if keys_pressed[pygame.K_d]:
        if xyellow + posuv + yellow.get_width() <= WIDTH // 2:
            xyellow += posuv
    if keys_pressed[pygame.K_w]:
        if yyellow - posuv >= 0:
            yyellow -= posuv
    if keys_pressed[pygame.K_s]:
        if yyellow + posuv + yellow.get_height() <= HEIGHT:
            yyellow += posuv

def pohyb_cerveneho(keys_pressed):
    global xred
    global yred
    if keys_pressed[pygame.K_LEFT]:
        if xred - posuv >= WIDTH // 2:
            xred -= posuv
    if keys_pressed[pygame.K_RIGHT]:
        if xred + posuv + red.get_width() <= WIDTH:
            xred += posuv
    if keys_pressed[pygame.K_UP]:
        if yred - posuv >= 0:
            yred -= posuv
    if keys_pressed[pygame.K_DOWN]:
        if yred + posuv + red.get_height() <= HEIGHT:
            yred += posuv
def draw_winner_text(text):
    WINNER_FONT  = pygame.font.SysFont('comicsans',80)
    draw_text = WINNER_FONT.render(text,1,CERVENA)
    screen.blit(draw_text,(WIDTH//2- draw_text.get_width()//2,HEIGHT//2-draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)

def kresli_zivot_laveho(text):
    HEALTH_FONT = pygame.font.SysFont('comicsans',20)
    draw_text = HEALTH_FONT.render(text,1,BIELA)
    screen.blit(draw_text,(0,0))


def kresli_zivot_praveho(text):
    HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
    draw_text = HEALTH_FONT.render(text, 1, BIELA)
    screen.blit(draw_text,( WIDTH-draw_text.get_width(), 0))



def kresli_instrukciu_laveho():
    FONT = pygame.font.SysFont('comicsans', 15)
    draw_text = FONT.render("STRELA = Lavy Ctrl, POHYB = WASD", 1, BIELA)
    screen.blit(draw_text, (150, 5))


def kresli_instrukci_praveho():
    FONT = pygame.font.SysFont('comicsans', 15)
    draw_text = FONT.render("STRELA = Pravy CTRL, POHYB = sipky", 1, BIELA)
    screen.blit(draw_text, (WIDTH - draw_text.get_width() - 150, 5))


class Strela:
    def __init__(self,x,y,polomer,rychlost,farba):
        self.x = x
        self.y = y
        self.polomer = polomer
        self.rychlost = rychlost
        self.farba = farba


    def updatni_polohu(self):
        self.x += self.rychlost

    def narazzlty(self):
        obdlznik = pygame.Rect(self.x, self.y, 2*self.polomer, 2*self.polomer)

        if obdlznik.colliderect(CERVENY_OBDLZNIK):
            global ZIVOT_LAVEHO
            ZIVOT_LAVEHO-=1

            return True

        if self.x < 0:
            return True

        return False

    def narazcerveny(self):
        obdlznik = pygame.Rect(self.x, self.y, 2*self.polomer, 2*self.polomer)

        if obdlznik.colliderect(ZLTY_OBDLZNIK):
            global ZIVOT_PRAVEHO
            ZIVOT_PRAVEHO-=1

            return True

        if self.x + self.polomer > WIDTH:
            return True


        return False


    def kresli(self):
        obdlznik = pygame.Rect(self.x, self.x, 2*self.polomer, 2*self.polomer)
        pygame.draw.circle(screen,self.farba,(self.x-self.polomer, self.y-self.polomer),self.polomer)


while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                gulka = Strela(xyellow+60,yyellow+35,10,BULL_SPEED,CERVENA)
                yellow_bullets.append(gulka)
                ZVUK2.play()

                #zlte gulky idu sprava dolava
            if event.key == pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:
                gulka = Strela(xred-10, yred+35,10, -BULL_SPEED,MODRA)
                #cervene idu zlava doprava
                red_bullets.append(gulka)
                ZVUK2.play()


    keys_pressed = pygame.key.get_pressed()
    pohyb_zlteho(keys_pressed)
    pohyb_cerveneho(keys_pressed)

    # cerveny je ten nalavo
    CERVENY_OBDLZNIK = pygame.Rect(xyellow, yyellow, yellow.get_width(), yellow.get_height())
    # zlty je ten napravo
    ZLTY_OBDLZNIK = pygame.Rect(xred, yred, red.get_width(), red.get_height())

    for cislo,i in enumerate(yellow_bullets):

        i.updatni_polohu()
        if i.narazcerveny():
            yellow_bullets.pop(cislo)

    for cislo,i in enumerate(red_bullets):

        i.updatni_polohu()
        if i.narazzlty():
            red_bullets.pop(cislo)

    draw_window()

    for i in yellow_bullets:
        i.kresli()

    for i in red_bullets:
        i.kresli()
    kresli_zivot_laveho("Zivoty: " + str(ZIVOT_LAVEHO))
    kresli_zivot_praveho("Zivoty: " + str(ZIVOT_PRAVEHO))
    kresli_instrukci_praveho()
    kresli_instrukciu_laveho()

    text = ""
    if ZIVOT_PRAVEHO==0:
        text = "Hrac nalavo vyhral !"
    elif ZIVOT_LAVEHO==0:
        text = "Hrac napravo vyhral !"
    if text != "":
        draw_winner_text(text)
        run = False

    pygame.display.update()
