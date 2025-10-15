import pygame
import sys
import random
import math

pygame.init()

# Constants

para = pygame.image.load("coin.png")
para_rect = para.get_rect()
para_rect.topleft = (300, 300)

canavar1 = pygame.image.load("canavar1.png")
canavar1_rect = canavar1.get_rect()
canavar1_rect.topleft = (100, 100)

arkaplan = pygame.image.load("background.png")
HIZ = 15
WIDTH, HEIGHT = 1400, 800
FPS = 180
pencere = pygame.display.set_mode((WIDTH, HEIGHT))

durum = True
score = 0
font = pygame.font.SysFont("Arial", 64)
BACKGROUND_COLOR = (0, 0, 0)

while(durum):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                durum = False

        
        pencere.fill(BACKGROUND_COLOR)

        
        pencere.blit(arkaplan, (0, 0))

        
        pencere.blit(canavar1, canavar1_rect)
        pencere.blit(para, para_rect)
        yazı = font.render("Puan: " + str(score), True, (255, 255, 255))
        pencere.blit(yazı, (10, 10))


        pygame.display.update()

        pygame.time.Clock().tick(FPS)

        tus = pygame.key.get_pressed()
        if tus[pygame.K_LEFT]:
            canavar1_rect.x -= HIZ
        elif tus[pygame.K_RIGHT]:
            canavar1_rect.x += HIZ
        elif tus[pygame.K_UP]:
            canavar1_rect.y -= HIZ
        elif tus[pygame.K_DOWN]:
            canavar1_rect.y += HIZ
        if canavar1_rect.colliderect(para_rect):
            para_rect.x = random.randint(0, WIDTH - para_rect.width)
            para_rect.y = random.randint(0, HEIGHT - para_rect.height)
            score += 1
        if score > 4:
             canavar1 = pygame.image.load("canavar2.png")


pygame.quit()