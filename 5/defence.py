import pygame as pg
import math


def calc_d(angle, length):
    dx = math.cos(angle) * length
    dy = math.sin(angle) * length
    return dx, dy


class Helicopter:
    def __init__(self, screen, speed, rotation):
        self.screen = screen
        self.speed = speed
        self.rotation = rotation

    def draw(self, ticks):
        y = 200
        x = ticks * self.speed // 512
        angle = (ticks * self.rotation // 128) % 360
        angle1 = angle / 180 * math.pi
        angle2 = ((angle + 90) % 360) / 180 * math.pi
        length = 50
        d1 = calc_d(angle1, length)
        d2 = calc_d(angle2, length)
        self.screen.fill('white')
        pg.draw.line(self.screen, 'red', (x - d1[0], y - d1[1]), (x + d1[0], y + d1[1]), 2)
        pg.draw.line(self.screen, 'red', (x - d2[0], y - d2[1]), (x + d2[0], y + d2[1]), 2)
        stick = 70
        pg.draw.line(self.screen, 'black', (x, y), (x, y + stick), 2)
        y += stick
        width = 100
        height = 100
        bound = pg.Rect(x - width, y, width*2, height)
        pg.draw.ellipse(self.screen, 'blue', bound, 2)
        y += height
        dist = 20
        stick = 30
        x -= dist
        pg.draw.line(self.screen, 'black', (x, y), (x, y + stick), 2)
        x += dist * 2
        pg.draw.line(self.screen, 'black', (x, y), (x, y + stick), 2)
        x -= dist + width
        y += stick
        pg.draw.line(self.screen, 'blue', (x, y), (x + width*2, y), 2)
        x += width * 2
        r = 30
        bound = pg.Rect(x - r//2, y - r, r, r)
        pg.draw.arc(self.screen, 'blue', bound, math.pi / 2 * 3, math.pi / 2 * 5, 1)


# Класс для окна
class Animation:
    # Инициализация
    def __init__(self, screen):
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.heli = Helicopter(screen, speed=100, rotation=70)

    # Запуск анимации
    def run(self):
        clock = pg.time.Clock()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    break
            else:
                tick = pg.time.get_ticks()
                self.heli.draw(tick)
                pg.display.flip()
            clock.tick(30)


# Основная функция программы
def main():
    width = 1400
    height = 800
    pg.init()
    screen = pg.display.set_mode((width, height))
    window = Animation(screen)
    window.run()
    pg.quit()


if __name__ == '__main__':
    main()
