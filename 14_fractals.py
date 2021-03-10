import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ----------  чтобы окно появлялось в верхнем левом углу ------------
x = 20
y = 40
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
# --------------------------------------------------------------------

pygame.init()

W = 1200
H = 600

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Множество Мандельброта")
sc.fill(WHITE)

FPS = 30        # число кадров в секунду
clock = pygame.time.Clock()

P = 200                     # размер [2*P+1 x 2*P+1]
scale = P / 0.5               # масштабный коэффициент
view = (0, -200)            # координаты смещения угла обзора
n_iter = 100                # число итераций для проверки принадлежности к множеству Мандельброта

for y in range(-P+view[1], P+view[1]):
    for x in range(-P+view[0], P+view[0]):
        a = x / scale
        b = y / scale
        c = complex(a, b)
        z = complex(0)
        n = 0
        for n in range(n_iter):
            z = z**2 + c
            if abs(z) > 2:
                break

        if n == n_iter-1:
            r = g = b = 0
        else:
            r = (n % 2) * 32 + 128
            g = (n % 4) * 64
            b = (n % 2) * 16 + 128

        pygame.draw.circle(sc, (r, g, b), (x + P - view[0], y + P - view[1]), 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()
    clock.tick(FPS)
