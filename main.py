import pygame

pygame.init()

window = pygame.display.set_mode((500, 500), pygame.RESIZABLE)

pygame.display.set_caption("Visualisation")

bg_color = (255, 255, 255)

window.fill(bg_color)
pygame.display.flip()

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
