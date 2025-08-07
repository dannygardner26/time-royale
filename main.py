import random

import pygame
import sys
from pygame.locals import *

import units

# set up the game
pygame.init()
WIDTH = 1000
HEIGHT = 400
running = True
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Clash Unroyale')
window.fill((255, 255, 255))
background = pygame.image.load("assets/images/background.png")
Friendly = []  # attacks tower B
Enemy = []  # attacks tower A
font = pygame.font.SysFont(None, 32)
game_time = 45  # seconds

card_images = [
    pygame.transform.scale(pygame.image.load("assets/images/knightcard.png"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/archercard.png"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/goblincard.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/giantcard.png"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/cannoncartcard.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/wizardcard.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/arrowscard.webp"), (60, 90))
]

# Scale up the small pixel images
tower_img = pygame.transform.scale(
    pygame.image.load("assets/images/castle1.png").convert_alpha(),
    (160, 240)  # The width and height of the castle image
)


def spellify(image_path: str, enemies, damage, radius, location, side=False):
    img = pygame.image.load(image_path).convert_alpha()
    window.blit(img, (location, HEIGHT - img.get_height() - 80))
    pygame.display.update()
    for enemy in enemies:
        if not enemy.dead:
            if abs(location - enemy.position) <= radius:
                enemy.takeDamage(damage)
    if side:
        if location - 100 <= radius:
            return damage
    else:
        if 820 - location <= radius:
            return damage
    return 0


def getTarget(side, enemies):
        if side:
            min = 100  # minimal distance from "me"
        else:
            min = 820
        for enemy in enemies:  # list of enemy units
            if not enemy.dead:
                if side:
                    if enemy.position > min:
                        min = enemy.position
                else:
                    if enemy.position < min:
                        min = enemy.position
        return min


# Displays the card selection menu and game over menu; QUIT event closes the game\
def show_menu(winner=None):
    global bot
    window.fill((255, 255, 255))
    selected_card = 0
    selected_cards = []
    selecting = winner is None

    while True:
        window.fill((255, 255, 255))
        if winner is None:
            title = font.render("CLASH UNROYALE", True, (0, 0, 0))
            prompt = font.render("< > to move, ENTER to select/deselect (max 4), SPACE to start, TAB to select bot level", True, (0, 0, 0))
            window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
            window.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 60))

            # Draw cards centered
            card_spacing = 20
            total_width = len(card_images) * 60 + (len(card_images) - 1) * card_spacing
            x = WIDTH // 2 - total_width // 2
            y = HEIGHT // 2
            for i, img in enumerate(card_images):
                window.blit(img, (x, y))
                # When the player clicks a card, it will be highlighted.
                if i == selected_card:
                    pygame.draw.rect(window, (255, 215, 0), (x - 4, y - 4, img.get_width() + 8, img.get_height() + 8),
                                     3)
                # Mark cards that are chosen
                if i in selected_cards:
                    pygame.draw.rect(window, (0, 200, 0), (x - 4, y - 4, img.get_width() + 8, img.get_height() + 8), 3)
                x += img.get_width() + card_spacing
            # Draw bot indicator
            if bot == 0:
                botimg = pygame.image.load("assets/images/robotoff.png")
            elif bot == 1:
                botimg = pygame.image.load("assets/images/roboteasy.png")
            elif bot == 2:
                botimg = pygame.image.load("assets/images/robotmedium.png")
            else:
                botimg = pygame.image.load("assets/images/robothard.png")
            window.blit(botimg, (0, 0))
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
            if selecting: # Allows the player to select cards
                if event.type == KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_card = (selected_card - 1) % len(card_images) # allows the player move between images to select diffrent cards
                    elif event.key == pygame.K_RIGHT:
                        selected_card = (selected_card + 1) % len(card_images)
                    elif event.key == pygame.K_RETURN:
                        if selected_card in selected_cards: # uses diffrent logic to select and deselect cards
                            selected_cards.remove(selected_card)
                        elif len(selected_cards) < 4:
                            selected_cards.append(selected_card)
                    elif event.key == pygame.K_SPACE and len(selected_cards) >= 1:
                        return selected_cards  # Start game with selected cards
                    elif event.key == pygame.K_TAB:
                        bot += 1
                        if bot > 3:
                            bot = 0
            else:
                if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                    return None  # Restarts game when someone loses


# runs the game; QUIT event returns user(s) to menu
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
    botid = -1


    def spawn(idx, elixer, side):
        if idx == 0 and elixer >= 3:
            if side:
                Enemy.append(
                    units.Units(random.random(), "assets/images/knightframe1.png", 170, 20, 36, 5, 12, side))
            else:
                Friendly.append(
                    units.Units(random.random(), "assets/images/knightframe1.png", 170, 20, 36, 5, 12, side))
            return 3, 0
        elif idx == 1 and elixer >= 3:
            if side:
                Enemy.append(
                    units.Units(random.random(), "assets/images/archersframe1.png", 30, 11, 27, 5, 50, side))
            else:
                Friendly.append(
                    units.Units(random.random(), "assets/images/archersframe1.png", 30, 11, 27, 5, 50, side))
            return 3, 0
        elif idx == 2 and elixer >= 2:
            if side:
                Enemy.append(
                    units.Units(random.random(), "assets/images/goblinframe1.png", 20, 12, 33, 10, 5, side))
            else:
                Friendly.append(
                    units.Units(random.random(), "assets/images/goblinframe1.png", 20, 12, 33, 10, 5, side))
            return 2, 0
        elif idx == 3 and elixer >= 5:
            if side:
                Enemy.append(
                    units.Units(random.random(), "assets/images/giantframe1.png", 200, 25, 45, 4, 12, side))
            else:
                Friendly.append(
                    units.Units(random.random(), "assets/images/giantframe1.png", 200, 25, 45, 4, 12, side))
            return 5, 0
        elif idx == 4 and elixer >= 4:
            if side:
                Enemy.append(
                    units.Units(random.random(), "assets/images/cannoncart.png", 180, 21, 27, 5, 55, side))
            else:
                Friendly.append(
                    units.Units(random.random(), "assets/images/cannoncart.png", 180, 21, 27, 5, 55, side))
            return 4, 0
        elif idx == 5 and elixer >= 5:
            if side:
                Enemy.append(
                    units.Units(random.random(), "assets/images/wizard.png", 75, 28, 42, 5, 55, side))
            else:
                Friendly.append(
                    units.Units(random.random(), "assets/images/wizard.png", 75, 28, 42, 5, 55, side))
            return 5, 0
        elif idx == 6 and elixer >= 3:
            if side:
                return 3, spellify("assets/images/arrows.png", Friendly, 36, 35, getTarget(side, Friendly), side)
            else:
                return 3, spellify("assets/images/arrows.png", Enemy, 36, 35, getTarget(side, Enemy), side)
        return 0, 0
    

    running = True
    while running:
        window.blit(background, (0, 0))

        # Draw towers at the very left and right ends
        window.blit(tower_img, (0, HEIGHT - tower_img.get_height() - 80))  # Left edge (Friendly tower)
        window.blit(tower_img,
                    (WIDTH - tower_img.get_width(), HEIGHT - tower_img.get_height() - 80))  # Right edge (Enemy tower)

        # Center positions for left and right player UI
        bar_width = 200
        bar_height = 20
        left_center_x = 200
        right_center_x = WIDTH - 200

        # Titles (centered)
        player1_text = font.render("Player 1", True, (0, 0, 0))
        if bot > 0:
            player2_text = font.render("Bot", True, (0, 0, 0))
        else:
            player2_text = font.render("Player 2", True, (0, 0, 0))
        window.blit(player1_text, (left_center_x - player1_text.get_width() // 2, 80))
        window.blit(player2_text, (right_center_x - player2_text.get_width() // 2, 80))

        # Health bars (centered)
        pygame.draw.rect(window, (255, 0, 0), (left_center_x - bar_width // 2, 20, bar_width * healthA / 300, 10))
        pygame.draw.rect(window, (255, 0, 0), (right_center_x - bar_width // 2, 20, bar_width * healthB / 300, 10))

        # Elixir bars (centered, under health bars)
        max_elixer = 10
        pygame.draw.rect(window, (128, 128, 128),
                         (left_center_x - bar_width // 2, 40, bar_width, bar_height))  # background left
        pygame.draw.rect(window, (102, 0, 204), (
            left_center_x - bar_width // 2, 40, int(bar_width * min(elixerA, max_elixer) / max_elixer),
            bar_height))  # fill left
        pygame.draw.rect(window, (128, 128, 128),
                         (right_center_x - bar_width // 2, 40, bar_width, bar_height))  # background right
        pygame.draw.rect(window, (204, 0, 102), (
            right_center_x - bar_width // 2, 40, int(bar_width * min(elixerB, max_elixer) / max_elixer),
            bar_height))  # fill right

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

        # updates and draws the freindly units
        for unit in Friendly:
            if unit.dead:
                Friendly.remove(unit)
            else:
                healthB -= unit.update(Enemy)
                window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height() - 80 - (unit.id * 5)))
        for unit in Enemy:
            if unit.dead:
                Enemy.remove(unit)
            else:
                healthA -= unit.update(Friendly)
            window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height() - 80 - (unit.id * 5)))
        if timer >= 20:
            amount = 2
            delixer = font.render("DOUBLE ELIXER", True, (200, 0, 255))
            window.blit(delixer, (WIDTH // 2 - delixer.get_width() // 2 - 5, 40))

        timer_text = font.render(f"Time: {int(time_left)}", True, (0, 0, 0))
        window.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 10))

        pygame.display.update()
        #  Controls the time passed in the game
        timePassed = clock.tick(30)
        timeSec = timePassed / 1000.0
        timer += timeSec
        elixerTime += timeSec
        # player.x += player.move * timeSec
        if elixerTime >= 1 / amount:
            elixerA += 1
            if bot == 0:
                elixerB += 1
            elif bot == 1:
                elixerB += 0.75
            elif bot == 2:
                elixerB += 1
            elif bot == 3:
                elixerB += 1.5
            elixerA = min(elixerA, max_elixer)
            elixerB = min(elixerB, max_elixer)
            elixerTime -= 1 / amount
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

        # spawning bot units; bot randomly chooses
        if bot > 0:
            if botid < 0:
                botid = selected_cards[random.randint(0, len(selected_cards)-1)]
                # print(botid, len(selected_cards))
            else:
                cost, tower = spawn(botid, elixerB, True)
                elixerB -= cost
                healthA -= tower
                if cost > 0:
                    botid = -1
        # spawning units; 1-4 for friendly (left); 7-0 for enemy (right);
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                # Only allow spawning the cards that were selected, using 1-4
                if event.key == pygame.K_1 and len(selected_cards) > 0:
                    idx = selected_cards[0]
                    cost, tower = spawn(idx, elixerA, False)
                    elixerA -= cost
                    healthB -= tower
                elif event.key == pygame.K_2 and len(selected_cards) > 1:
                    idx = selected_cards[1]
                    cost, tower = spawn(idx, elixerA, False)
                    elixerA -= cost
                    healthB -= tower
                elif event.key == pygame.K_3 and len(selected_cards) > 2:
                    idx = selected_cards[2]
                    cost, tower = spawn(idx, elixerA, False)
                    elixerA -= cost
                    healthB -= tower
                elif event.key == pygame.K_4 and len(selected_cards) > 3:
                    idx = selected_cards[3]
                    cost, tower = spawn(idx, elixerA, False)
                    elixerA -= cost
                    healthB -= tower
                # Enemy card spawning (using keys 7-0)
                if not bot:
                    if event.key == pygame.K_7 and len(selected_cards) > 0:
                        idx = selected_cards[0]
                        cost, tower = spawn(idx, elixerB, True)
                        elixerB -= cost
                        healthA -= tower
                    elif event.key == pygame.K_8 and len(selected_cards) > 1:
                        idx = selected_cards[1]
                        cost, tower = spawn(idx, elixerB, True)
                        elixerB -= cost
                        healthA -= tower
                    elif event.key == pygame.K_9 and len(selected_cards) > 2:
                        idx = selected_cards[2]
                        cost, tower = spawn(idx, elixerB, True)
                        elixerB -= cost
                        healthA -= tower
                    elif event.key == pygame.K_0 and len(selected_cards) > 3:
                        idx = selected_cards[3]
                        cost, tower = spawn(idx, elixerB, True)
                        elixerB -= cost
                        healthA -= tower

        # Check for game over
        if healthA <= 0 or healthB <= 0:
            winner = 2 if healthA <= 0 else 1
            return winner  # Exit the loop and return the winner


pygame.display.update()
bot = 0

# --- Main program starts here ---
while True:
    selected_cards = show_menu()
    winner = run_game(selected_cards)  # Run the game with those cards
    show_menu(winner)
    # After game ends, show menu with winner and repeat
