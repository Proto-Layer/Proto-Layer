import random
import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector

# Choose which animation to display:
# Options: 'waves', 'glowbugs', 'flakes', 'flames'
ANIMATION_MODE = "glowbugs"  # Switch this to change the effect

# --- Expanding Wave (Ripple) Effect ---
class Wave:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.duration = 2.0
        self.time_alive = 0.0

    def update(self, dt) -> bool:
        self.time_alive += dt
        if self.time_alive > self.duration:
            return False
        growth = self.time_alive / self.duration
        self.radius = 100 * growth
        return True

    def render(self, canvas):
        fade = 1.0 - (self.time_alive / self.duration)
        with canvas:
            Color(1, 1, 1, fade)
            Line(circle=(self.x, self.y, self.radius), width=2)

class WaveWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.waves = []
        Clock.schedule_interval(self.refresh, 1 / 60.)
        self.queue_next()

    def queue_next(self):
        delay = random.uniform(0.5, 1.5)
        Clock.schedule_once(self.spawn_wave, delay)

    def spawn_wave(self, dt):
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        self.waves.append(Wave(x, y))
        self.queue_next()

    def refresh(self, dt):
        self.canvas.clear()
        if len(self.waves) > 50:
            self.waves = self.waves[-50:]
        for wave in self.waves[:]:
            if wave.update(dt):
                wave.render(self.canvas)
            else:
                self.waves.remove(wave)

# --- Firefly / Glowbug Effect ---
class Glowbug:
    def __init__(self):
        self.x = random.uniform(0, Window.width)
        self.y = random.uniform(0, Window.height)
        self.velocity = Vector(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        self.blink_interval = random.uniform(0.5, 2.0)
        self.time_alive = 0.0
        self.visible = True

    def update(self, dt):
        self.time_alive += dt
        if self.time_alive > self.blink_interval:
            self.visible = not self.visible
            self.time_alive = 0.0
            self.blink_interval = random.uniform(0.5, 2.0)
        self.x = (self.x + self.velocity.x) % Window.width
        self.y = (self.y + self.velocity.y) % Window.height

    def render(self, canvas):
        if self.visible:
            with canvas:
                Color(1, 1, 0.5)
                Ellipse(pos=(self.x - 2, self.y - 2), size=(4, 4))

class GlowbugWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bugs = [Glowbug() for _ in range(50)]
        Clock.schedule_interval(self.refresh, 1 / 60.)

    def refresh(self, dt):
        self.canvas.clear()
        for bug in self.bugs:
            bug.update(dt)
            bug.render(self.canvas)

# --- Snowfall Effect ---
class Flake:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.size = random.uniform(2, 5)
        self.fall_speed = random.uniform(-2, -1)
        self.wind = random.uniform(-0.5, 0.5)
        self.width = width
        self.height = height

    def update(self, dt):
        self.y += self.fall_speed
        self.x += self.wind
        if self.y < 0:
            self.y = self.height
            self.x = random.uniform(0, self.width)
        return True

    def render(self, canvas):
        with canvas:
            Color(1, 1, 1)
            Ellipse(pos=(self.x, self.y), size=(self.size, self.size))

class SnowWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flakes = [
            Flak
