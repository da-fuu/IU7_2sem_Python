import pygame as pg
import math


# Расчет позиции на орбите по периоду и фазе
def calc_pos_in_orbit(center, rad, phase, period):
    angle = (phase % period) / period * 2 * math.pi
    x = math.cos(angle) * rad
    y = math.sin(angle) * rad
    return center[0] + y, center[1] + x


# Расчет левого верхнего угла квадрата по центру и стороне
def calc_sprite_pos(center, rad):
    return center[0] - rad // 2, center[1] - rad // 2


# Класс для окна
class Animation:
    # Инициализация
    def __init__(self):
        self.WIDTH = self.HEIGHT = self.SUN_POS = None
        self.sun = self.earth = self.moon = self.space = None
        self.rects = ()
        self.stage = None

        self.SUN_RAD = 140
        self.EARTH_RAD = 50
        self.MOON_RAD = 20

        self.EARTH_ORBIT = 300
        self.MOON_ORBIT = 80

        self.EARTH_PERIOD = 365
        self.MOON_PERIOD = 29
        self.DAYS_IN_SEC = 20

    # Загрузка спрайтов
    def load_images(self):
        self.sun = pg.image.load('images/sun.png')
        self.sun = pg.transform.scale(self.sun, (self.SUN_RAD, self.SUN_RAD))

        self.earth = pg.image.load('images/earth.png')
        self.earth = pg.transform.scale(self.earth, (self.EARTH_RAD, self.EARTH_RAD))

        self.moon = pg.image.load('images/moon.png')
        self.moon = pg.transform.scale(self.moon, (self.MOON_RAD, self.MOON_RAD))

        self.space = pg.image.load('images/bg.png')
        self.space = pg.transform.scale(self.space, (self.WIDTH, self.HEIGHT))

    # Расчет периода в мс
    def calc_period(self, period_in_days):
        return period_in_days * 1000 // self.DAYS_IN_SEC

    # Переход ко второй стадии анимации
    def goto_2_stage(self):
        self.earth = pg.image.load('images/boom.png')
        self.EARTH_RAD = 60
        self.earth = pg.transform.scale(self.earth, (self.EARTH_RAD, self.EARTH_RAD))
        self.stage = 2

    # Обновление поверхностей
    def update_surface(self, screen, ticks):
        rects = ()
        if self.stage == 0:
            screen.blit(self.space, (0, 0))
            screen.blit(self.sun, calc_sprite_pos(self.SUN_POS, self.SUN_RAD))
            earth_pos = calc_pos_in_orbit(self.SUN_POS, self.EARTH_ORBIT, ticks, self.calc_period(self.EARTH_PERIOD))
            new_earth_rect = screen.blit(self.earth, calc_sprite_pos(earth_pos, self.EARTH_RAD))
            moon_pos = calc_pos_in_orbit(earth_pos, self.MOON_ORBIT, ticks, self.calc_period(self.MOON_PERIOD))
            new_moon_rect = screen.blit(self.moon, calc_sprite_pos(moon_pos, self.MOON_RAD))
            rects = (new_moon_rect, new_earth_rect)
            if ticks > 5000:
                self.stage = 1
        elif self.stage == 1:
            screen.blit(self.space, (0, 0))
            screen.blit(self.sun, calc_sprite_pos(self.SUN_POS, self.SUN_RAD))
            earth_pos = calc_pos_in_orbit(self.SUN_POS, self.EARTH_ORBIT, ticks, self.calc_period(self.EARTH_PERIOD))
            moon_pos = calc_pos_in_orbit(earth_pos, self.MOON_ORBIT, ticks, self.calc_period(self.MOON_PERIOD))
            new_moon_rect = screen.blit(self.moon, calc_sprite_pos(moon_pos, self.MOON_RAD))
            new_earth_rect = screen.blit(self.earth, calc_sprite_pos(earth_pos, self.EARTH_RAD))
            rects = (new_moon_rect, new_earth_rect)
            self.MOON_ORBIT -= 1
            if self.MOON_ORBIT < self.EARTH_RAD // 2:
                self.goto_2_stage()
        elif self.stage == 2:
            screen.blit(self.space, (0, 0))
            earth_pos = calc_pos_in_orbit(self.SUN_POS, self.EARTH_ORBIT, ticks, self.calc_period(self.EARTH_PERIOD))
            new_earth_rect = screen.blit(self.earth, calc_sprite_pos(earth_pos, self.EARTH_RAD))
            screen.blit(self.sun, calc_sprite_pos(self.SUN_POS, self.SUN_RAD))
            rects = (new_earth_rect, )
            self.EARTH_ORBIT -= 1
            if self.EARTH_ORBIT < self.SUN_RAD // 2 - 20:
                self.stage = 3
        elif self.stage == 3:
            screen.blit(self.space, (0, 0))
            sun_pos = screen.blit(self.sun, calc_sprite_pos(self.SUN_POS, self.SUN_RAD))
            self.rects = (sun_pos, )
            self.SUN_POS[0] += 1
        return rects

    # Запуск анимации
    def run(self, screen):
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.load_images()
        self.rects = (pg.Rect(0, 0, self.WIDTH, self.HEIGHT), )
        self.SUN_POS = [self.WIDTH // 2, self.HEIGHT // 2]
        clock = pg.time.Clock()
        running = True
        self.stage = 0
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    break
            else:
                tick = pg.time.get_ticks()
                new_rects = self.update_surface(screen, tick)
                pg.display.update(new_rects + self.rects)
                self.rects = new_rects
            clock.tick(30)


# Основная функция программы
def main():
    width = 1400
    height = 800
    pg.init()
    screen = pg.display.set_mode((width, height))
    window = Animation()
    window.run(screen)
    pg.quit()


if __name__ == '__main__':
    main()
