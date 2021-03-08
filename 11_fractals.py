import pygame
import numpy as np
import os
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class SIF:
    def __init__(self, coeffs):
        self.coeffs = coeffs
        self.T = self.create_funcs()
        self.P = self.get_probabilities()


    def create_funcs(self):
        T = []
        for c in self.coeffs:
            t = np.array(c[:4]).reshape(2, 2)
            h = np.array(c[4:])
            T.append((t, h))

        return T

    def create_attractor(self, surf_e, n_iter):
        size = surf_e.get_size()

        surf_res = pygame.Surface(size)
        surf_iter = pygame.Surface(size)

        surf_res.blit(surf_e, (0, 0))

        size_np = np.array(size)
        for n in range(n_iter):
            surf_iter.fill(WHITE)
            for t in self.T:
                size_scale = np.int32(np.round(t[0] @ size_np))
                offset = np.int32(np.round( t[1] * size_np))
                s = pygame.transform.smoothscale(surf_res, size_scale)
                surf_iter.blit(s, offset)

            surf_res.blit(surf_iter, (0, 0))

        return surf_res

    def get_random_T(self, pr):
        p = random.random()  # случайное вещественное число в интервале [0; 1]
        off = 0
        for i, pt in enumerate(pr):
            if p < (pt+off):
                return self.T[i]
            off += pt

        return False

    def get_probabilities(self):
        dets = [np.abs(np.linalg.det(t[0])) + 0.1 for t in self.T]
        s = sum(dets)
        return [d/s for d in dets]

    def get_next_point(self, pos, pt, scale):
        p = self.get_probabilities()
        t = self.get_random_T(p)

        if not t:
            return pt

        pt_new = t[0] @ pt + t[1] * scale + pos
        return (pt_new[0], pt_new[1])



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

surf_e = pygame.Surface((200, 200))
surf_e.fill(BLACK)
pygame.draw.rect(surf_e, WHITE, surf_e.get_rect(), 60)

C = [(0.5, 0, 0, 0.5, 0, 0),
     (0.5, 0, 0, 0.5, 0.5, 0),
     (0.5, 0, 0, 0.5, 0.25, 0.433),
]

sif = SIF(C)
pt = (0, 0)
scale = (200, 200)
pos = (100, 100)


FPS = 30        # число кадров в секунду
clock = pygame.time.Clock()

n_iter = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    if n_iter < 1000:
        pygame.draw.circle(sc, BLACK, (round(pt[0]), round(pt[1])), 2)
        pt = sif.get_next_point( pos, pt, scale )
        n_iter += 1

    pygame.display.update()
    clock.tick(FPS)
