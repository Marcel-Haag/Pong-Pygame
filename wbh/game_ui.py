# pygame objects and color
import pygame
from pygame.locals import *
import sys

BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


def main():
    windowWidth = 300
    windowHeight = 250
    running = True
    windowResolution = (windowWidth, windowHeight)
    backgroundColor = BLUE  # rgb defined color

    colorGreen = pygame.Color('green')

    rectx1 = 10
    recty1 = 10
    rectwidth1 = 20
    rectheight1 = 20

    rect1 = (rectx1, recty1, rectwidth1, rectheight1)

    # init pygame, define display surface and 
    # set a title for the window
    pygame.init()

    displaySurface = \
        pygame.display.set_mode(windowResolution)

    pygame.display.set_caption('Fun with PyGame!')

    # infinite loop − stop running with escape key 
    # or by closing the window
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # draw four objects with methods from pygame
        displaySurface.fill(backgroundColor)

        pygame.draw.rect(displaySurface,
                         (colorGreen), rect1, 0)

        pygame.draw.circle(displaySurface,
                           RED, (80, 80), 30)

        pygame.draw.ellipse(displaySurface,
                            YELLOW, (100, 150, 50, 25), 0)

        pygame.draw.line(displaySurface,
                         WHITE, (220, 160), (160, 220))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
