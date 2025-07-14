import pygame, sys, time, random, math
from pygame.math import Vector2 as vec
from .text_tools import *
pygame.init()

font = pygame.font.SysFont('couriernew', 30)
button_font = pygame.font.SysFont('arial', 50)
title_font = pygame.font.SysFont('ArialRounded', 80)
W,H = 1500, 1000
enemy_base_speed = 100
diag = (W**2 + H**2)**0.5

def cos(theta):
    return math.cos(math.radians(theta))

def sin(theta):
    return -math.sin(math.radians(theta))

def debug(item, pos = (10,10)):
    screen = pygame.display.get_surface()
    text = str(item)
    img = font.render(text, True, 'white')
    rect = img.get_rect(topleft = pos)

    pygame.draw.rect(screen, 'black', rect)
    screen.blit(img, rect)

def cartesian(r, theta):
    return vec(r * cos(theta), r * sin(theta))

def check_arc_collision(lower_angle, upper_angle, out_rad, in_rad, center, point):
    #distance check
    dist = vec(point).distance_to(vec(center))
    angle = vec(1,0).angle_to(vec(point[0], -point[1]) - vec(center[0], -center[1]))%360

    if not (in_rad <= dist <= out_rad):
        return False
    
    #angle check
    if lower_angle > upper_angle:  #x axis lies between them
        upper_angle += 360
        if point[1] <= center[1]: #point is below the x axis
            angle += 360
    if not (lower_angle <= angle <= upper_angle):
        return False
        
    return True

def circle_to_circle_collision(c1, c2, r1, r2):
    return (vec(c1).distance_to(vec(c2)) <= (r1 + r2))

def draw_aa_arc(screen, bbox: pygame.Rect, start_angle, end_angle, width, color, bgcolor='black'):
    surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    #drawing outer circle
    pygame.draw.aacircle(surf, color, bbox.center, bbox.width/2, width)
    #drawing cutting arc
    pygame.draw.arc(surf, bgcolor, bbox.inflate(5,5), end_angle, start_angle, width + 5)
    #drawing lines
    ...

    surf.set_colorkey(bgcolor)
    screen.blit(surf, (0,0))


def draw_aa_arc2(screen, bbox: pygame.Rect, start_angle, end_angle, width, color, bgcolor = 'black'):
    surf = pygame.Surface((screen.get_width()*3, screen.get_height()*3), pygame.SRCALPHA)
    surf.set_colorkey(bgcolor)

    rect = bbox.inflate(bbox.width * 2, bbox.height * 2)

    rect.center = (surf.get_width()/2, surf.get_height()/2)

    pygame.draw.arc(surf, color, rect, start_angle, end_angle, width*3)
    surf = pygame.transform.smoothscale(surf, (screen.get_width(), screen.get_height()))
    screen.blit(surf, (0,0))