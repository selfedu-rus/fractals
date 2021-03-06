import pygame
import numpy as np
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class SIF:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def create_funcs(self):
        T = []
        for c in self.coeffs:
            t = np.array(c[:4]).reshape(2, 2)
            h = np.array(c[4:])
            T.append((t, h))

        return T

    def create_attractor(self, surf_e, n_iter):
        size = surf_e.get_size()
        T = self.create_funcs()

        surf_res = pygame.Surface(size)
        surf_iter = pygame.Surface(size)

        surf_res.blit(surf_e, (0, 0))

        size_np = np.array(size)
        for n in range(n_iter):
            surf_iter.fill(WHITE)
            for t in T:
                size_scale = np.int32(np.round(t[0] @ size_np))
                offset = np.int32(np.round( t[1] * size_np))
                s = pygame.transform.smoothscale(surf_res, size_scale)
                surf_iter.blit(s, offset)

            surf_res.blit(surf_iter, (0, 0))

        return surf_res


# ----------  чтобы окно появлялось в верхнем левом углу ------------
x = 20
y = 40
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
# --------------------------------------------------------------------

pygame.init()

W = 1200
H = 600

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Система итерированных функций")
sc.fill(WHITE)

FPS = 30        # число кадров в секунду
clock = pygame.time.Clock()

surf_e = pygame.Surface((200, 200))
surf_e.fill(BLACK)
pygame.draw.rect(surf_e, WHITE, surf_e.get_rect(), 60)

C = [(0.5, 0, 0, 0.5, 0, 0),
     (0.5, 0, 0, 0.5, 0.5, 0),
     (0.5, 0, 0, 0.5, 0.25, 0.433),
]

sif = SIF(C)
surf_res = sif.create_attractor(surf_e, 0)
surf_res = pygame.transform.flip(surf_res, False, True)

n_iter = 1
step = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    step += 1
    if step > 30 and n_iter < 8:
        step = 0
        surf_res = sif.create_attractor(surf_e, n_iter)
        surf_res = pygame.transform.flip(surf_res, False, True)
        n_iter += 1

    sc.blit(surf_res, (100, 200))
    pygame.display.update()

    clock.tick(FPS)
