import pygame

import time
import random

pygame.init()

# Display size
display_width = 800
display_height = 600
car_width = 73
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("A bit racey!")  # gameCaption
clock = pygame.time.Clock()

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)

pause = False

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
block_color = (53, 115, 255)
# Car image
carImg = pygame.image.load("racecar.png")


def things_dodged(count):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def thing_2(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font("freesansbold.ttf", 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def crash():
    crash = True
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("You Crashed!", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while crash:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # gameDisplay.fill(white)

        button("Again", 150, 450, 100, 50, green, bright_green, game_loop)
        button("QUIT", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def quit_game():
    pygame.quit()
    quit()


def unpause():
    global pause
    pause = False


def paused():
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("Paused!", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # gameDisplay.fill(white)

        button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
        button("QUIT", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("QUIT", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    # for thing 1
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    # for thing 2
    thing_startx2 = random.randrange(0, display_width)
    thing_starty2 = -600
    thing_speed2 = 5
    thing_width2 = 100
    thing_height2 = 100

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        gameDisplay.fill(white)  # displaying white colour on the screen

        # thing 1
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed

        # thing 2
        thing_2(thing_startx2, thing_starty2, thing_width2, thing_height2, block_color)
        thing_starty2 += thing_speed2
        car(x, y)  # displaying car image on the screen
        things_dodged(dodged)
        if x > display_width - car_width or x < 0:  # Boundaries
            crash()

        """if value of block is greater than display height.. meaning -600 after adding 7 7 to it it will eventually be gre
        ater than display height which is 600px. so then execute the code"""

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 0.4
            thing_width += (dodged * 1.04)
        if thing_starty2 > display_height:
            thing_starty2 = 0 - thing_height2
            thing_startx2 = random.randrange(0, display_width)
            dodged += 1
            thing_speed2 += 0.4
            thing_width2 += (dodged * 1.02)
        # Collision
        # collision(y, thing_starty, thing_height, thing_startx, thing_width, thing_startx, car_width)
        if y < thing_starty + thing_height:
            print ("y crossover")
            if thing_startx < x < thing_startx + thing_width or thing_startx < x + car_width < thing_startx \
                    + thing_width:
                print ("x crossover")
                crash()
        if y < thing_starty2 + thing_height2:
            print ("y crossover")
            if thing_startx2 < x < thing_startx2 + thing_width2 or thing_startx2 < x + car_width < thing_startx2 \
                    + thing_width2:
                print ("x crossover")
                crash()

        pygame.display.update()  # Update Screen
        clock.tick(90)  # fps


game_intro()

game_loop()

pygame.quit()

quit()