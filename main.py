import random

import pygame
import sys
from pygame.locals import *

from assets.units import archer, cannoncart, giant, goblin, knight, wizard

# Set up the game
pygame.init()
WIDTH = 1000
HEIGHT = 400
running = True
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Clash Unroyale')
window.fill((255, 255, 255))
background = pygame.image.load("assets/images/background.png")
font = pygame.font.SysFont(None, 32)
gameTime = 45  # seconds

cardImages = [
    pygame.transform.scale(pygame.image.load("assets/images/knightcard.png"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/archercard.png"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/goblincard.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/giantcard.png"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/cannoncartcard.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/wizardcard.webp"), (60, 90)),
    pygame.transform.scale(pygame.image.load("assets/images/arrowscard.webp"), (60, 90))
]

# Scale up the small pixel images
towerImg = pygame.transform.scale(
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
def showMenu(winner=None):
    global bot
    window.fill((255, 255, 255))
    selectedCard = 0
    selectedCards = []
    selecting = winner is None

    while True:
        window.fill((255, 255, 255))
        if winner is None:
            title = font.render("CLASH UNROYALE", True, (0, 0, 0))
            prompt = font.render("< > to move, ENTER to select/deselect (max 4), SPACE to start, TAB to select bot level", True, (0, 0, 0))
            window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
            window.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 60))

            # Draw cards centered
            cardSpacing = 20
            totalWidth = len(cardImages) * 60 + (len(cardImages) - 1) * cardSpacing
            x = WIDTH // 2 - totalWidth // 2
            y = HEIGHT // 2
            for i, img in enumerate(cardImages):
                window.blit(img, (x, y))
                # When the player clicks a card, it will be highlighted.
                if i == selectedCard:
                    pygame.draw.rect(window, (255, 215, 0), (x - 4, y - 4, img.get_width() + 8, img.get_height() + 8),
                                     3)
                # Mark cards that are chosen
                if i in selectedCards:
                    pygame.draw.rect(window, (0, 200, 0), (x - 4, y - 4, img.get_width() + 8, img.get_height() + 8), 3)
                x += img.get_width() + cardSpacing
            # Draw bot indicator
            if bot == 0:
                botImg = pygame.image.load("assets/images/robotoff.png")
            elif bot == 1:
                botImg = pygame.image.load("assets/images/roboteasy.png")
            elif bot == 2:
                botImg = pygame.image.load("assets/images/robotmedium.png")
            else:
                botImg = pygame.image.load("assets/images/robothard.png")
            window.blit(botImg, (0, 0))
        else:
            if winner == "No one":
                winText = font.render("Draw!", True, (0, 0, 0))
            else:
                winText = font.render(f"Player {winner} Wins!", True, (0, 128, 0))
            prompt = font.render("Press SPACE to Restart", True, (0, 0, 0))
            window.blit(winText, (WIDTH // 2 - winText.get_width() // 2, HEIGHT // 2 - 60))
            window.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if selecting:  # Allows the player to select cards
                if event.type == KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # allows the player move between images to select different cards
                        selectedCard = (selectedCard - 1) % len(cardImages)
                    elif event.key == pygame.K_RIGHT:
                        selectedCard = (selectedCard + 1) % len(cardImages)
                    elif event.key == pygame.K_RETURN:
                        if selectedCard in selectedCards:  # uses different logic to select and deselect cards
                            selectedCards.remove(selectedCard)
                        elif len(selectedCards) < 4:
                            selectedCards.append(selectedCard)
                    elif event.key == pygame.K_SPACE and len(selectedCards) >= 1:
                        return selectedCards  # Start game with selected cards
                    elif event.key == pygame.K_TAB:
                        bot += 1
                        if bot > 3:
                            bot = 0
            else:
                if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                    return None  # Restarts game when someone loses


# runs the game; QUIT event returns user(s) to menu
def run_game(selectedCards):
    # Reset game state
    healthA = 300
    healthB = 300
    elixerA = 0
    elixerB = 0
    friendly = []
    enemy = []
    timer = 0
    elixerTime = 0
    amount = 1
    timeLeft = gameTime
    botId = -1

    def spawn(idx, elixer, side):
        if idx == 0 and elixer >= 3:
            if side:
                enemy.append(knight.Knight(random.random(), side))
            else:
                friendly.append(knight.Knight(random.random(), side))
            return 3, 0
        elif idx == 1 and elixer >= 3:
            if side:
                enemy.append(archer.Archer(random.random(), side))
            else:
                friendly.append(archer.Archer(random.random(), side))
            return 3, 0
        elif idx == 2 and elixer >= 2:
            if side:
                enemy.append(goblin.Goblin(random.random(), side))
            else:
                friendly.append(goblin.Goblin(random.random(), side))
            return 2, 0
        elif idx == 3 and elixer >= 5:
            if side:
                enemy.append(giant.Giant(random.random(), side))
            else:
                friendly.append(giant.Giant(random.random(), side))
            return 5, 0
        elif idx == 4 and elixer >= 4:
            if side:
                enemy.append(cannoncart.CannonCart(random.random(), side))
            else:
                friendly.append(cannoncart.CannonCart(random.random(), side))
            return 4, 0
        elif idx == 5 and elixer >= 5:
            if side:
                enemy.append(wizard.Wizard(random.random(), side))
            else:
                friendly.append(wizard.Wizard(random.random(), side))
            return 5, 0
        elif idx == 6 and elixer >= 3:
            if side:
                return 3, spellify("assets/images/arrows.png", friendly, 36, 70, getTarget(side, friendly), side)
            else:
                return 3, spellify("assets/images/arrows.png", enemy, 36, 70, getTarget(side, enemy), side)
        return 0, 0

    running = True
    while running:
        window.blit(background, (0, 0))

        # Draw towers at the very left and right ends
        window.blit(towerImg, (0, HEIGHT - towerImg.get_height() - 80))  # Left edge (Friendly tower)
        window.blit(towerImg,
                    (WIDTH - towerImg.get_width(), HEIGHT - towerImg.get_height() - 80))  # Right edge (Enemy tower)

        # Center positions for left and right player UI
        barWidth = 200
        barHeight = 20
        leftCenterX = 200
        rightCenterX = WIDTH - 200

        # Titles (centered)
        player1Text = font.render("Player 1", True, (0, 0, 0))
        if bot > 0:
            player2Text = font.render("Bot", True, (0, 0, 0))
        else:
            player2Text = font.render("Player 2", True, (0, 0, 0))
        window.blit(player1Text, (leftCenterX - player1Text.get_width() // 2, 80))
        window.blit(player2Text, (rightCenterX - player2Text.get_width() // 2, 80))

        # Health bars (centered)
        pygame.draw.rect(window, (255, 0, 0), (leftCenterX - barWidth // 2, 20, barWidth * healthA / 300, 10))
        pygame.draw.rect(window, (255, 0, 0), (rightCenterX - barWidth // 2, 20, barWidth * healthB / 300, 10))

        # Elixir bars (centered, under health bars)
        maxElixer = 10
        pygame.draw.rect(window, (128, 128, 128),
                         (leftCenterX - barWidth // 2, 40, barWidth, barHeight))  # background left
        pygame.draw.rect(window, (102, 0, 204), (
            leftCenterX - barWidth // 2, 40, int(barWidth * min(elixerA, maxElixer) / maxElixer),
            barHeight))  # fill left
        pygame.draw.rect(window, (128, 128, 128),
                         (rightCenterX - barWidth // 2, 40, barWidth, barHeight))  # background right
        pygame.draw.rect(window, (204, 0, 102), (
            rightCenterX - barWidth // 2, 40, int(barWidth * min(elixerB, maxElixer) / maxElixer),
            barHeight))  # fill right

        # Cards (centered, below bars)
        cardSpacing = 20
        cardWidth = 60
        totalWidth = len(selectedCards) * cardWidth + (len(selectedCards) - 1) * cardSpacing
        x = WIDTH // 2 - totalWidth // 2
        y = 130  # below the bars

        for idx in selectedCards:
            img = cardImages[idx]
            window.blit(img, (x, y))
            x += img.get_width() + cardSpacing

        # updates and draws the freindly units
        for unit in friendly:
            if unit.dead:
                friendly.remove(unit)
            else:
                healthB -= unit.update(enemy)
                window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height() - 80 - (unit.id * 5)))
        for unit in enemy:
            if unit.dead:
                enemy.remove(unit)
            else:
                healthA -= unit.update(friendly)
            window.blit(unit.image, (unit.position, HEIGHT - unit.image.get_height() - 80 - (unit.id * 5)))
        if timer >= 20:
            amount = 2
            delixer = font.render("DOUBLE ELIXER", True, (200, 0, 255))
            window.blit(delixer, (WIDTH // 2 - delixer.get_width() // 2 - 5, 40))

        timerText = font.render(f"Time: {int(timeLeft)}", True, (0, 0, 0))
        window.blit(timerText, (WIDTH // 2 - timerText.get_width() // 2, 10))

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
            elixerA = min(elixerA, maxElixer)
            elixerB = min(elixerB, maxElixer)
            elixerTime -= 1 / amount
            print(elixerA, elixerB)

        timeLeft -= timeSec
        if timeLeft <= 0 or healthA <= 0 or healthB <= 0:
            if timeLeft <= 0:
                if healthA == healthB:
                    winner = "No one"
                else:
                    winner = 1 if healthA > healthB else 2
            else:
                winner = 2 if healthA <= 0 else 1
            return winner  # Exit the loop and return the winner

        # spawning bot units; bot randomly chooses
        if bot > 0:
            if botId < 0:
                botId = selectedCards[random.randint(0, len(selectedCards)-1)]
                # print(botid, len(selected_cards))
            else:
                cost, tower = spawn(botId, elixerB, True)
                elixerB -= cost
                healthA -= tower
                if cost > 0:
                    botId = -1
        # spawning units; 1-4 for friendly (left); 7-0 for enemy (right);
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                # Only allow spawning the cards that were selected, using 1-4
                if event.key == pygame.K_1 and len(selectedCards) > 0:
                    idx = selectedCards[0]
                    cost, tower = spawn(idx, elixerA, False)
                    elixerA -= cost
                    healthB -= tower
                elif event.key == pygame.K_2 and len(selectedCards) > 1:
                    idx = selectedCards[1]
                    cost, tower = spawn(idx, elixerA, False)
                    elixerA -= cost
                    healthB -= tower
                elif event.key == pygame.K_3 and len(selectedCards) > 2:
                    idx = selectedCards[2]
                    cost, tower = spawn(idx, elixerA, False)
                    elixerA -= cost
                    healthB -= tower
                elif event.key == pygame.K_4 and len(selectedCards) > 3:
                    idx = selectedCards[3]
                    cost, tower = spawn(idx, elixerA, False)
                    elixerA -= cost
                    healthB -= tower
                # Enemy card spawning (using keys 7-0)
                if bot == 0:
                    if event.key == pygame.K_7 and len(selectedCards) > 0:
                        idx = selectedCards[0]
                        cost, tower = spawn(idx, elixerB, True)
                        elixerB -= cost
                        healthA -= tower
                    elif event.key == pygame.K_8 and len(selectedCards) > 1:
                        idx = selectedCards[1]
                        cost, tower = spawn(idx, elixerB, True)
                        elixerB -= cost
                        healthA -= tower
                    elif event.key == pygame.K_9 and len(selectedCards) > 2:
                        idx = selectedCards[2]
                        cost, tower = spawn(idx, elixerB, True)
                        elixerB -= cost
                        healthA -= tower
                    elif event.key == pygame.K_0 and len(selectedCards) > 3:
                        idx = selectedCards[3]
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
    selectedCards = showMenu()
    winner = run_game(selectedCards)  # Run the game with those cards
    showMenu(winner)
    # After game ends, show menu with winner and repeat
