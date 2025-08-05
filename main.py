import pygame, sys
from pygame.locals import*
import units
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
Friendly  = [] # attacks tower B
Enemy = [] # attacks tower A
healthA = 100
healthB = 100

# Draw an 8x8 pixel rectangle at position (50, 300)
pygame.draw.rect(window, (255, 0, 0), (50, 300, 8, 8))
class Player():
    def __init__(self):
        self.size = 20
        self.speed = 250
        self.move = 0
        self.height = 50
        self.width = 100
        self.x = WIDTH / 2 - self.size / 2
        self.y = HEIGHT - self.height
        self.image = pygame.Surface((self.width, self.height)).convert()
        self.image.fill((0, 255, 255))

player = Player()

card_images = [
    pygame.transform.scale(pygame.image.load("assets\images\OIP.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets\images\OIP (1).webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets\images\Gobs.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/Giant.png"), (60, 90)),
]

pygame.display.update()
while running:
    window.fill((255, 255, 255))
    # Display all card images in a row with spacing
    card_spacing = 20
    x = 50
    y = 10
    for img in card_images:
        window.blit(img, (x, y))
        x += img.get_width() + card_spacing
    
    # Update and draw all friendly units (knights)
    for unit in Friendly:
        if unit.dead:
            Friendly.remove(unit)
        else:
            healthB -= unit.update(Enemy)  # or knight.update() if you want to use your update logic
            window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height()))
    for unit in Enemy:
        if unit.dead:
            Enemy.remove(unit)
        else:
            healthA -= unit.update(Friendly)  # or knight.update() if you want to use your update logic
            window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height()))
    # Tower A / Friendly tower
    pygame.draw.rect(window, (255, 0, 0), (100, 100, healthA, 10))
    # Tower B / Enemy tower
    pygame.draw.rect(window, (255, 0, 0), (800, 100, healthB, 10))

    pygame.display.update()

    timePassed = clock.tick(30)
    timeSec = timePassed / 1000.0
    player.x += player.move * timeSec

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN: # speeds can't be relative primes
            if event.key == pygame.K_1:
                Friendly.append(units.Units(1, "assets/images/pixil-gif-drawing.gif", 100, 10, 10, 5, 100, False))
            elif event.key == pygame.K_2:
                Enemy.append(units.Units(2, "assets\images\pixil-gif-drawing (1).gif", 65, 8, 15, 10, 100, True))
            elif event.key == pygame.K_3:
                player.move = -player.speed
            elif event.key == pygame.K_4:
                player.move = -player.speed
        

pygame.quit()
sys.exit()
