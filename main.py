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
background = pygame.image.load("assets/images/background.png")
Friendly  = [] # attacks tower B
Enemy = [] # attacks tower A
healthA = 300
healthB = 300
elixerA = 0 # friendly elixer
elixerB = 0 # enemy elixer
# Draw an 8x8 pixel rectangle at position (50, 300)
pygame.draw.rect(window, (255, 0, 0), (50, 300, 8, 8))
font = pygame.font.SysFont(None, 32)
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

tower_img = pygame.transform.scale(
    pygame.image.load("assets/images/castle1.png").convert_alpha(),
    (160, 240)  # width, height (adjust as needed to be bigger than the giant)
)

def show_menu(winner=None):
    window.fill((255, 255, 255))
    if winner is None:
        title = font.render("TIME ROYALE", True, (0, 0, 0))
        prompt = font.render("Press SPACE to Start", True, (0, 0, 0))
        window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
        window.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
    else:
        win_text = font.render(f"Player {winner} Wins!", True, (0, 128, 0))
        prompt = font.render("Press SPACE to Restart", True, (0, 0, 0))
        window.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 60))
        window.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

pygame.display.update()
timer = 0
elixerTime = 0
amount = 1

# --- Main program starts here ---
show_menu()  # Show menu before starting the game

while running:
    window.blit(background, (0, 0))

    # Draw towers at the very left and right ends
    window.blit(tower_img, (0, HEIGHT - tower_img.get_height() - 80))  # Left edge (Friendly tower)
    window.blit(tower_img, (WIDTH - tower_img.get_width(), HEIGHT - tower_img.get_height() - 80))  # Right edge (Enemy tower)

    # Center positions for left and right player UI
    bar_width = 200
    bar_height = 20
    left_center_x = 200
    right_center_x = WIDTH - 200

    # Titles (centered)
    player1_text = font.render("Player 1", True, (0, 0, 0))
    player2_text = font.render("Player 2", True, (0, 0, 0))
    window.blit(player1_text, (left_center_x - player1_text.get_width() // 2, 40))
    window.blit(player2_text, (right_center_x - player2_text.get_width() // 2, 40))

    # Health bars (centered)
    pygame.draw.rect(window, (255, 0, 0), (left_center_x - bar_width // 2, 70, bar_width * healthA / 300, 10))
    pygame.draw.rect(window, (255, 0, 0), (right_center_x - bar_width // 2, 70, bar_width * healthB / 300, 10))

    # Elixir bars (centered, under health bars)
    max_elixer = 10
    pygame.draw.rect(window, (128, 128, 128), (left_center_x - bar_width // 2, 90, bar_width, bar_height))  # background left
    pygame.draw.rect(window, (102, 0, 204), (left_center_x - bar_width // 2, 90, int(bar_width * min(elixerA, max_elixer) / max_elixer), bar_height))  # fill left
    pygame.draw.rect(window, (128, 128, 128), (right_center_x - bar_width // 2, 90, bar_width, bar_height))  # background right
    pygame.draw.rect(window, (204, 0, 102), (right_center_x - bar_width // 2, 90, int(bar_width * min(elixerB, max_elixer) / max_elixer), bar_height))  # fill right

    # Cards (centered, below bars)
    card_spacing = 20
    total_width = len(card_images) * 60 + (len(card_images) - 1) * card_spacing
    x = WIDTH // 2 - total_width // 2
    y = 130  # below the bars
    for img in card_images:
        window.blit(img, (x, y))
        x += img.get_width() + card_spacing

    # Update and draw all friendly units (knights)
    for unit in Friendly:
        if unit.dead:
            Friendly.remove(unit)
        else:
            healthB -= unit.update(Enemy)  # or knight.update() if you want to use your update logic
            window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height()-80))
    for unit in Enemy:
        if unit.dead:
            Enemy.remove(unit)
        else:
            healthA -= unit.update(Friendly)
            window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height()-80))

    # Health bars (optional, drawn above towers)
    pygame.draw.rect(window, (255, 0, 0), (100, 100, healthA/3, 10))
    pygame.draw.rect(window, (255, 0, 0), (800, 100, healthB/3, 10))

    # Elixir bar settings
    max_elixer = 10
    bar_width = 200
    bar_height = 20

    # Friendly elixir bar (under health bar, left)
    pygame.draw.rect(window, (128, 128, 128), (100, 120, bar_width, bar_height))  # background
    pygame.draw.rect(window, (102, 0, 204), (100, 120, int(bar_width * min(elixerA, max_elixer) / max_elixer), bar_height))  # fill

    # Enemy elixir bar (under health bar, right)
    pygame.draw.rect(window, (128, 128, 128), (800, 120, bar_width, bar_height))  # background
    pygame.draw.rect(window, (204, 0, 102), (800, 120, int(bar_width * min(elixerB, max_elixer) / max_elixer), bar_height))  # fill

    pygame.display.update()
    timePassed = clock.tick(30)
    timeSec = timePassed / 1000.0
    timer += timeSec
    elixerTime += timeSec
    player.x += player.move * timeSec
    if timer >= 20:
        amount = 2
    if elixerTime >= 1/amount:
        elixerA += 1
        elixerB += 1
        elixerA = min(elixerA, max_elixer)
        elixerB = min(elixerB, max_elixer)
        elixerTime -= 1/amount
        print(elixerA, elixerB)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN: # speeds can't be relative primes
            if event.key == pygame.K_1 and elixerA >= 3:
                Friendly.append(units.Units(1, "assets\images\knightframe1.png", 100, 10, 10, 5, 10, False))
                elixerA -= 3
            elif event.key == pygame.K_2 and elixerA >= 3:
                Friendly.append(units.Units(2, "assets/images/archersframe1.png", 65, 8, 12, 6, 200, False))     
                elixerA -= 3       
            elif event.key == pygame.K_3 and elixerA >= 2:
                Friendly.append(units.Units(3, "assets\images\goblinframe1.png", 50, 5, 15, 15, 8, False))
                elixerA -= 2    
            elif event.key == pygame.K_4 and elixerA >= 5:
                Friendly.append(units.Units(4, "assets\images\giantframe1.png", 200, 15, 5, 4, 5, False))
                elixerA -= 5
                ##GOOD GUYS^^
                ##BAD GUYS VVV
            elif event.key == pygame.K_7 and elixerB >= 3:    
                Enemy.append(units.Units(5, "assets\images\knightframe1.png", 100, 10, 10, 5, 10, True))
                elixerB -= 3
            elif event.key == pygame.K_8 and elixerB >= 3:
                Enemy.append(units.Units(6, "assets/images/archersframe1.png", 65, 8, 12, 6, 200, True))
                elixerB -= 3     
            elif event.key == pygame.K_9 and elixerB >= 2:
                Enemy.append(units.Units(7, "assets\images\goblinframe1.png", 50, 5, 15, 15, 8, True))
                elixerB -= 2
            elif event.key == pygame.K_0 and elixerB >= 5:
                Enemy.append(units.Units(8, "assets\images\giantframe1.png", 200, 15, 5, 4, 5, True))
                elixerB -= 5

    # Check for game over
    if healthA <= 0 or healthB <= 0:
        winner = 2 if healthA <= 0 else 1
        show_menu(winner)
        # Reset game state
        healthA = 300
        healthB = 300
        elixerA = 0
        elixerB = 0
        Friendly.clear()
        Enemy.clear()
        timer = 0
        elixerTime = 0
        amount = 1

pygame.quit()
sys.exit()
