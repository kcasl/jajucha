
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D 파티클 효과")

def draw_particle(x, y, z):
    glBegin(GL_POINTS)
    glVertex3f(x, y, z)
    glEnd()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # 파티클을 그리는 루프
        for i in range(1000):
            x, y, z = 10,10,10  # 파티클의 위치 계산
            draw_particle(x, y, z)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
