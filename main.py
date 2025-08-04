import pygame, sys
from pygame.locals import*
#i am julius
pygame.init()
WIDTH = 1000
HEIGHT = 400
running = True
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Python is cool!')
window.fill((255, 255, 255))
back = pygame.Surface((WIDTH, HEIGHT))
background = back.convert()
background.fill((255, 255, 255))

healthA = 100
healthB = 100

# Draw an 8x8 pixel rectangle at position (50, 300)
pygame.draw.rect(window, (255, 0, 0), (50, 300, 8, 8))
class Player():
    size = 20

    speed = 250
    move = 0
    height = 50
    width = 100

    x = WIDTH / 2 - size / 2
    y = HEIGHT - height

    image = pygame.Surface((width, height)).convert()
    image.fill((0, 255, 255))

player = Player()

card_image = pygame.image.load("assets/images/OIP.webp")

while running:
    pygame.display.update()
    window.blit(background, (0, 0))
    
    window.blit(card_image, (player.x, player.y))
    
      # Draw an 8x8 pixel rectangle at position (50, 300)
    pygame.draw.rect(window, (255, 0, 0), (50, 300, 8, 8))
    
    window.blit(card_image, (50, 300))
    
    pygame.display.update()
    # ...rest of your loop...
    
    timePassed = clock.tick(30)
    timeSec = timePassed / 1000.0
    player.x += player.move * timeSec
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.move = player.speed
            elif event.key == K_LEFT:
                player.move = -player.speed
        elif event.type == KEYUP:
            if event.key == K_LEFT or K_RIGHT:
                player.move = 0

pygame.quit()
sys.exit()
