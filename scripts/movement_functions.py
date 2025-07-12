from .utils import *


def radially_outward(speed, angle, dt):
    dx = speed * dt * cos(angle)
    dy = speed * dt * sin(angle)

    return dx, dy


def track(pos, point, speed, dt):
    direction = vec(point) - vec(pos)

    if not direction.length(): return (0,0)

    return direction.normalize() * speed * dt


def sine_wave_towards(pos, point, speed, amplitude, dt):
    direction = vec(point) - vec(pos)