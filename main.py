import pygame, sys
from pygame.locals import*
import units
import random
#i am julius
pygame.init()
WIDTH = 1000
HEIGHT = 400
running = True
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Clash Unroyale')
window.fill((255, 255, 255))
background = pygame.image.load("assets/images/background.png")
Friendly  = [] # attacks tower B
Enemy = [] # attacks tower A
healthA = 300
healthB = 300
elixerA = 2 # friendly elixer
elixerB = 2 # enemy elixer
font = pygame.font.SysFont(None, 32)
game_time = 45  # seconds
time_left = game_time
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
    pygame.transform.scale(pygame.image.load("assets/images/OIP.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/OIP (1).webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/Gobs.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/Giant.png"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets\images\CannonCart.webp"), (60, 90)),  # <-- Cannon Cart here
]

tower_img = pygame.transform.scale(
    pygame.image.load("assets/images/castle1.png").convert_alpha(),
    (160, 240)  # width, height (adjust as needed to be bigger than the giant)
)

def show_menu(winner=None):
    window.fill((255, 255, 255))
    selected_card = 0
    selected_cards = []
    selecting = winner is None

    while True:
        window.fill((255, 255, 255))
        if winner is None:
            title = font.render("CLASH UNROYALE", True, (0, 0, 0))
            prompt = font.render("Use ← → to move, ENTER to select/deselect (max 4), SPACE to start", True, (0, 0, 0))
            window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
            window.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 60))

            # Draw cards centered
            card_spacing = 20
            total_width = len(card_images) * 60 + (len(card_images) - 1) * card_spacing
            x = WIDTH // 2 - total_width // 2
            y = HEIGHT // 2
            for i, img in enumerate(card_images):
                window.blit(img, (x, y))
                # Highlight selected card
                if i == selected_card:
                    pygame.draw.rect(window, (255, 215, 0), (x-4, y-4, img.get_width()+8, img.get_height()+8), 3)
                # Mark cards that are chosen
                if i in selected_cards:
                    pygame.draw.rect(window, (0, 200, 0), (x-4, y-4, img.get_width()+8, img.get_height()+8), 3)
                x += img.get_width() + card_spacing
        else:
            if winner == "No one":
                win_text = font.render("Draw!", True, (0, 0, 0))
            else:
                win_text = font.render(f"Player {winner} Wins!", True, (0, 128, 0))
            prompt = font.render("Press SPACE to Restart", True, (0, 0, 0))
            window.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 60))
            window.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if selecting:
                if event.type == KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_card = (selected_card - 1) % len(card_images)
                    elif event.key == pygame.K_RIGHT:
                        selected_card = (selected_card + 1) % len(card_images)
                    elif event.key == pygame.K_RETURN:
                        if selected_card in selected_cards:
                            selected_cards.remove(selected_card)
                        elif len(selected_cards) < 4:
                            selected_cards.append(selected_card)
                    elif event.key == pygame.K_SPACE and len(selected_cards) >= 1:
                        return selected_cards  # Start game with selected cards
            else:
                if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                    return None  # Restart game

pygame.display.update()
timer = 0
elixerTime = 0
amount = 1

def run_game(selected_cards):
    global healthA, healthB, elixerA, elixerB, timer, elixerTime, amount, time_left, Friendly, Enemy
    # Reset game state
    healthA = 300
    healthB = 300
    elixerA = 0
    elixerB = 0
    Friendly = []
    Enemy = []
    timer = 0
    elixerTime = 0
    amount = 1
    time_left = game_time

    running = True
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
        window.blit(player1_text, (left_center_x - player1_text.get_width() // 2, 80))
        window.blit(player2_text, (right_center_x - player2_text.get_width() // 2, 80))

        # Health bars (centered)
        pygame.draw.rect(window, (255, 0, 0), (left_center_x - bar_width // 2, 20, bar_width * healthA / 300, 10))
        pygame.draw.rect(window, (255, 0, 0), (right_center_x - bar_width // 2, 20, bar_width * healthB / 300, 10))

        # Elixir bars (centered, under health bars)
        max_elixer = 10
        pygame.draw.rect(window, (128, 128, 128), (left_center_x - bar_width // 2, 40, bar_width, bar_height))  # background left
        pygame.draw.rect(window, (102, 0, 204), (left_center_x - bar_width // 2, 40, int(bar_width * min(elixerA, max_elixer) / max_elixer), bar_height))  # fill left
        pygame.draw.rect(window, (128, 128, 128), (right_center_x - bar_width // 2, 40, bar_width, bar_height))  # background right
        pygame.draw.rect(window, (204, 0, 102), (right_center_x - bar_width // 2, 40, int(bar_width * min(elixerB, max_elixer) / max_elixer), bar_height))  # fill right

        # Cards (centered, below bars)
        card_spacing = 20
        card_width = 60
        total_width = len(selected_cards) * card_width + (len(selected_cards) - 1) * card_spacing
        x = WIDTH // 2 - total_width // 2
        y = 130  # below the bars

        for idx in selected_cards:
            img = card_images[idx]
            window.blit(img, (x, y))
            x += img.get_width() + card_spacing

        # Update and draw all friendly units (knights)
        for unit in Friendly:
            if unit.dead:
                Friendly.remove(unit)
            else:
                healthB -= unit.update(Enemy)  # or knight.update() if you want to use your update logic
                window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height()-80-(unit.id*5)))
        for unit in Enemy:
            if unit.dead:
                Enemy.remove(unit)
            else:
                healthA -= unit.update(Friendly)
            window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height()-80-(unit.id*5)))
        if timer >= 20:
            amount = 2
            delixer = font.render("DOUBLE ELIXER", True, (0, 0, 0))
            window.blit(delixer, (WIDTH // 2 - delixer.get_width() // 2 - 5, 20))

        timer_text = font.render(f"Time: {int(time_left)}", True, (0, 0, 0))
        window.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 10))

        pygame.display.update()
        # The following block was incorrectly indented; fix indentation
        timePassed = clock.tick(30)
        timeSec = timePassed / 1000.0
        timer += timeSec
        elixerTime += timeSec
        player.x += player.move * timeSec
        if elixerTime >= 1/amount:
            elixerA += 1
            elixerB += 1
            elixerA = min(elixerA, max_elixer)
            elixerB = min(elixerB, max_elixer)
            elixerTime -= 1/amount
            print(elixerA, elixerB)

        time_left -= timeSec
        if time_left <= 0 or healthA <= 0 or healthB <= 0:
            if time_left <= 0:
                if healthA == healthB:
                    winner = "No one"
                else:
                    winner = 1 if healthA > healthB else 2
            else:
                winner = 2 if healthA <= 0 else 1
            return winner  # Exit the loop and return the winner

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                    # Only allow spawning the cards that were selected, using 1-4
                    if event.key == pygame.K_1 and len(selected_cards) > 0:
                        idx = selected_cards[0]
                        if idx == 0 and elixerA >= 3:
                            Friendly.append(units.Units(1, "assets/images/knightframe1.png", 70, 10, 10, 5, 10, False))
                            elixerA -= 3
                        elif idx == 1 and elixerA >= 3:
                            Friendly.append(units.Units(2, "assets/images/archersframe1.png", 60, 5, 12, 6, 200, False))
                            elixerA -= 3
                        elif idx == 2 and elixerA >= 2:
                            Friendly.append(units.Units(3, "assets/images/goblinframe1.png", 50, 5, 15, 15, 8, False))
                            elixerA -= 2
                        elif idx == 3 and elixerA >= 5:
                            Friendly.append(units.Units(4, "assets/images/giantframe1.png", 100, 8, 20, 2, 5, False))
                            elixerA -= 5
                        elif idx == 4 and elixerA >= 4:  # Cannon Cart (example cost: 4)
                            Friendly.append(units.Units(
                                5,  # unique id for cannon cart
                                "assets/images/cannoncart.png",
                                80,   # health (example)
                                12,   # damage (example)
                                15,   # attackRate (example)
                                6,    # speed (example)
                                120,  # range (example)
                                False
                            ))
                            elixerA -= 4
                    elif event.key == pygame.K_2 and len(selected_cards) > 1:
                        idx = selected_cards[1]
                        if idx == 0 and elixerA >= 3:
                            Friendly.append(units.Units(1, "assets/images/knightframe1.png", 70, 10, 10, 5, 10, False))
                            elixerA -= 3
                        elif idx == 1 and elixerA >= 3:
                            Friendly.append(units.Units(2, "assets/images/archersframe1.png", 60, 5, 12, 6, 200, False))
                            elixerA -= 3
                        elif idx == 2 and elixerA >= 2:
                            Friendly.append(units.Units(3, "assets/images/goblinframe1.png", 50, 5, 15, 15, 8, False))
                            elixerA -= 2
                        elif idx == 3 and elixerA >= 5:
                            Friendly.append(units.Units(4, "assets/images/giantframe1.png", 100, 8, 20, 2, 5, False))
                            elixerA -= 5
                        elif idx == 4 and elixerA >= 4:  # Cannon Cart (example cost: 4)
                            Friendly.append(units.Units(
                                5,  # unique id for cannon cart
                                "assets/images/cannoncart.png",
                                80,   # health (example)
                                12,   # damage (example)
                                15,   # attackRate (example)
                                6,    # speed (example)
                                120,  # range (example)
                                False
                            ))
                            elixerA -= 4
                    elif event.key == pygame.K_3 and len(selected_cards) > 2:
                        idx = selected_cards[2]
                        if idx == 0 and elixerA >= 3:
                            Friendly.append(units.Units(1, "assets/images/knightframe1.png", 70, 10, 10, 5, 10, False))
                            elixerA -= 3
                        elif idx == 1 and elixerA >= 3:
                            Friendly.append(units.Units(2, "assets/images/archersframe1.png", 60, 5, 12, 6, 200, False))
                            elixerA -= 3
                        elif idx == 2 and elixerA >= 2:
                            Friendly.append(units.Units(3, "assets/images/goblinframe1.png", 50, 5, 15, 15, 8, False))
                            elixerA -= 2
                        elif idx == 3 and elixerA >= 5:
                            Friendly.append(units.Units(4, "assets/images/giantframe1.png", 100, 8, 20, 2, 5, False))
                            elixerA -= 5
                        elif idx == 4 and elixerA >= 4:  # Cannon Cart (example cost: 4)
                            Friendly.append(units.Units(
                                5,  # unique id for cannon cart
                                "assets/images/cannoncart.png",
                                80,   # health (example)
                                12,   # damage (example)
                                15,   # attackRate (example)
                                6,    # speed (example)
                                120,  # range (example)
                                False
                            ))
                            elixerA -= 4
                    elif event.key == pygame.K_4 and len(selected_cards) > 3:
                        idx = selected_cards[3]
                        if idx == 0 and elixerA >= 3:
                            Friendly.append(units.Units(1, "assets/images/knightframe1.png", 70, 10, 10, 5, 10, False))
                            elixerA -= 3
                        elif idx == 1 and elixerA >= 3:
                            Friendly.append(units.Units(2, "assets/images/archersframe1.png", 60, 5, 12, 6, 200, False))
                            elixerA -= 3
                        elif idx == 2 and elixerA >= 2:
                            Friendly.append(units.Units(3, "assets/images/goblinframe1.png", 50, 5, 15, 15, 8, False))
                            elixerA -= 2
                        elif idx == 3 and elixerA >= 5:
                            Friendly.append(units.Units(4, "assets/images/giantframe1.png", 100, 8, 20, 2, 5, False))
                            elixerA -= 5
                        elif idx == 4 and elixerA >= 4:  # Cannon Cart (example cost: 4)
                            Friendly.append(units.Units(
                                5,  # unique id for cannon cart
                                "assets/images/cannoncart.png",
                                80,   # health (example)
                                12,   # damage (example)
                                15,   # attackRate (example)
                                6,    # speed (example)
                                120,  # range (example)
                                False
                            ))
                            elixerA -= 4
                    # Enemy card spawning (using keys 5-8)
                    if event.key == pygame.K_5 and len(selected_cards) > 0:
                        idx = selected_cards[0]
                        if idx == 0 and elixerB >= 3:
                            Enemy.append(units.Units(1, "assets/images/knightframe1.png", 70, 10, 10, 5, 10, True))
                            elixerB -= 3
                        elif idx == 1 and elixerB >= 3:
                            Enemy.append(units.Units(2, "assets/images/archersframe1.png", 60, 5, 12, 6, 200, True))
                            elixerB -= 3
                        elif idx == 2 and elixerB >= 2:
                            Enemy.append(units.Units(3, "assets/images/goblinframe1.png", 50, 5, 15, 15, 8, True))
                            elixerB -= 2
                        elif idx == 3 and elixerB >= 5:
                            Enemy.append(units.Units(4, "assets/images/giantframe1.png", 100, 8, 20, 2, 5, True))
                            elixerB -= 5
                        elif idx == 4 and elixerB >= 4:  # Cannon Cart (example cost: 4)
                            Enemy.append(units.Units(
                                5,
                                "assets/images/cannoncart.png",
                                80,  # health
                                12,  # damage
                                15,  # attackRate
                                6,   # speed
                                120, # range
                                True
                            ))
                            elixerB -= 4
                    elif event.key == pygame.K_6 and elixerB >= 3 and len(selected_cards) > 1:
                        idx = selected_cards[1]
                        if idx == 0:
                            Enemy.append(units.Units(1, "assets/images/knightframe1.png", 70, 10, 10, 5, 10, True))
                            elixerB -= 3
                        elif idx == 1:
                            Enemy.append(units.Units(2, "assets/images/archersframe1.png", 60, 5, 12, 6, 200, True))
                            elixerB -= 3
                        elif idx == 2:
                            Enemy.append(units.Units(3, "assets/images/goblinframe1.png", 50, 5, 15, 15, 8, True))
                            elixerB -= 2
                        elif idx == 3:
                            Enemy.append(units.Units(4, "assets/images/giantframe1.png", 100, 8, 20, 2, 5, True))
                            elixerB -= 5
                        elif idx == 4 and elixerB >= 4:  # Cannon Cart (example cost: 4)
                            Enemy.append(units.Units(
                                5,
                                "assets/images/cannoncart.png",
                                80,  # health
                                12,  # damage
                                15,  # attackRate
                                6,   # speed
                                120, # range
                                True
                            ))
                            elixerB -= 4
                    elif event.key == pygame.K_7 and elixerB >= 2 and len(selected_cards) > 2:
                        idx = selected_cards[2]
                        if idx == 0:
                            Enemy.append(units.Units(1, "assets/images/knightframe1.png", 70, 10, 10, 5, 10, True))
                            elixerB -= 3
                        elif idx == 1:
                            Enemy.append(units.Units(2, "assets/images/archersframe1.png", 60, 5, 12, 6, 200, True))
                            elixerB -= 3
                        elif idx == 2:
                            Enemy.append(units.Units(3, "assets/images/goblinframe1.png", 50, 5, 15, 15, 8, True))
                            elixerB -= 2
                        elif idx == 3:
                            Enemy.append(units.Units(4, "assets/images/giantframe1.png", 100, 8, 20, 2, 5, True))
                            elixerB -= 5
                        elif idx == 4 and elixerB >= 4:  # Cannon Cart (example cost: 4)
                            Enemy.append(units.Units(
                                5,
                                "assets/images/cannoncart.png",
                                80,  # health
                                12,  # damage
                                15,  # attackRate
                                6,   # speed
                                120, # range
                                True
                            ))
                            elixerB -= 4
                    elif event.key == pygame.K_8 and elixerB >= 5 and len(selected_cards) > 3:
                        idx = selected_cards[3]
                        if idx == 0:
                            Enemy.append(units.Units(1, "assets/images/knightframe1.png", 70, 10, 10, 5, 10, True))
                            elixerB -= 3
                        elif idx == 1:
                            Enemy.append(units.Units(2, "assets/images/archersframe1.png", 60, 5, 12, 6, 200, True))
                            elixerB -= 3
                        elif idx == 2:
                            Enemy.append(units.Units(3, "assets/images/goblinframe1.png", 50, 5, 15, 15, 8, True))
                            elixerB -= 2
                        elif idx == 3:
                            Enemy.append(units.Units(4, "assets/images/giantframe1.png", 100, 8, 20, 2, 5, True))
                            elixerB -= 5
                        elif idx == 4 and elixerB >= 4:  # Cannon Cart (example cost: 4)
                            Enemy.append(units.Units(
                                5,
                                "assets/images/cannoncart.png",
                                80,  # health
                                12,  # damage
                                15,  # attackRate
                                6,   # speed
                                120, # range
                                True
                            ))
                            elixerB -= 4

        # Check for game over
        if healthA <= 0 or healthB <= 0:
            winner = 2 if healthA <= 0 else 1
            return winner  # Exit the loop and return the winner

# --- Main program starts here ---
while True:
    selected_cards = show_menu()  # Show menu and get selected cards
    winner = run_game(selected_cards)  # Run the game with those cards
    # After game ends, show menu with winner and repeat

pygame.quit()
sys.exit()
