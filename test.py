import pygame

pygame.init()

window = pygame.display.set_mode((500, 500), pygame.RESIZABLE)

pygame.display.set_caption("Visualisation")

bg_color = (255, 255, 255)

window.fill(bg_color)
pygame.display.flip()

rect_1_color = (255, 0, 255)

rect_1_rect = pygame.Rect((10, 10), (100, 100))

rect_1_width = 0

pygame.draw.rect(window, rect_1_color, rect_1_rect, rect_1_width)

pygame.display.flip()

while 1:
    window.fill(bg_color)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            rect_1_rect.left += 1
            rect_1_rect.right += 1
            pygame.draw.rect(window, rect_1_color, rect_1_rect, rect_1_width)
            pygame.display.update()
            pygame.display.flip()
