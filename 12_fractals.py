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

surf_draw = pygame.Surface((W, H))
surf_draw.fill(WHITE)

C = [(0.195, -0.488, 0.344, 0.443, 0.4431, 0.2452),
     (0.462, 0.414, -0.252, 0.361, 0.2511, 0.5692),
     (-0.058, -0.07, 0.453, -0.111, 0.5976, 0.0969),
     (-0.035, 0.07, -0.469, 0.022, 0.4884, 0.5069),
     (-0.637, 0.0, 0.0, 0.501, 0.8562, 0.2513),
]

color = (79, 42, 15)

sif = SIF(C)
pt = (0, 0)
scale = (400, 400)
pos = (0, 0)

f_sys = pygame.font.SysFont('arial', 36)
sc_text = f_sys.render(f'Итерация: 0', 1, BLACK)


FPS = 30        # число кадров в секунду
clock = pygame.time.Clock()

n_iter = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    if n_iter < 100000:
        pygame.draw.circle(surf_draw, color, (round(pt[0]), round(pt[1])), 0)
        pt = sif.get_next_point( pos, pt, scale )
        n_iter += 1

        if n_iter % 100 == 0:
            sc_text = f_sys.render(f'Итерация: {n_iter}', 1, BLACK)

        sc.blit(pygame.transform.flip(surf_draw, False, True), (200, -100))
        pygame.draw.rect(sc, WHITE, sc_text.get_rect(topleft=(50, 20)))
        sc.blit( sc_text, (50, 20))


    pygame.display.update()
    clock.tick(FPS)
