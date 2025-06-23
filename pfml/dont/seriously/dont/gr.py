import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['PFML_DEBUG_MODE'] = "hide"

import pygame
from typing import IO, Union, Tuple, Sequence, Any
from pygame.math import Vector2
from pygame.color import Color
import sys
from os import PathLike
from pathlib import Path

AnyPath = Union[str, bytes, PathLike[str], PathLike[bytes]]

FileArg = Union[AnyPath, IO[bytes], IO[str]]

String = str

RGBAOutput = Tuple[int, int, int, int]

uint = int

Vector2i = Tuple[int, int]
Vector2u = Tuple[uint, uint]
Vector2f = Tuple[float, float]

Drawable = list[pygame.Surface, Vector2f, bool]

Drawble = Any

IntRect = Tuple[Vector2i, Vector2i]

ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]

file_path = Path(__file__)
gr_parent = file_path.parent

class lntRect():
    def __new__(self, rect: IntRect):
        return rect

class VideoMode():
    """VideoMode defines a video mode (size, bpp)"""
    
    def __new__(self, size: Vector2):
        return size

class BetterWindow:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.og_screen_size = self.surface.get_size()
        self._is_open = True
        self.current_screen_sprites = []

    def close(self):
        self._is_open = False
        pygame.quit()
        sys.exit()
    
    def isOpen(self) -> bool:
        return self._is_open
    
    def clear(self, color: ColorValue = (0, 0, 0)):
        self.surface.fill(color)
        self.current_screen_sprites.clear()
    
    def display(self):
        pygame.display.flip()
        self.current_screen_size = self.surface.get_size()
        # SORTOWANIE PO Y!
        for sprite in sorted(self.current_screen_sprites, key=lambda s: s.pos[1]):
            sprite.tick(self.current_screen_size, self.og_screen_size)
    
    
    
    def draw(self, drawable: Drawble):
        self.surface.blit(drawable.sprite_shown, drawable.pos)
        self.current_screen_sprites.append(drawable)
    
    def pollEvent(self):
        return pygame.event.get()
    
    def getSize(self):
        return self.surface.get_size()
    
    # Expose Surface methods using __getattr__
    def __getattr__(self, name):
        return getattr(self.surface, name)


class Window():
    """Construct a new window
    
    This constructor creates the window with the size and pixel
    depth defined in `mode`. An optional style can be passed to
    customize the look and behavior of the window (borders,
    title bar, resizable, closable, ...). An optional state can
    be provided. If `state` is `State::Fullscreen`, then `mode`
    must be a valid video mode.
    
    The last parameter is an optional structure specifying
    advanced OpenGL context settings such as anti-aliasing,
    depth-buffer bits, etc.
    
    Parameters:
        mode (VideoMode): Video mode to use (defines the width, height and depth of the rendering area of the window)
        title (String): Title of the window
    """
    
    def __new__(self, mode: VideoMode, title: String):
        screen = pygame.display.set_mode(mode, pygame.RESIZABLE)
        pygame.display.set_caption(title)
        
        icon = pygame.image.load(f"{gr_parent}\\none_program_icon-3.png")
        pygame.display.set_icon(icon)
        
        return BetterWindow(screen)

class BetterImage():
    def __init__(self, image: pygame.Surface, sRgb: bool):
        self.image = image
        self.sRgb = sRgb
        self.smoothingness = False
    
    def get_size(self) -> Vector2u:
        return self.image.get_size()
    
    def setSmooth(self, smooth: bool):
        self.smoothingness = smooth
    
    def isSrgb(self) -> bool:
        return self.sRgb

texture = BetterImage

class Texture():
    """Image living on the graphics card that can be used for drawing"""
    
    def __new__(self, filename: FileArg):
        image = pygame.image.load(filename)
        return BetterImage(image, False)
    
    def __new__(self, filename: FileArg, sRgb: bool, area: IntRect):
        image = pygame.image.load(filename)
        rect = pygame.Rect(area[0][0], area[0][1], area[1][0], area[1][1])
        sprite = image.subsurface(rect)
        image = sprite
        return BetterImage(image, sRgb)

class BetterSprite():
    def __init__(self, sprite: Drawable):
        self.sprite = sprite[0]
        self.sprite_shown = self.sprite
        self.pos = sprite[1]
        self.sprite_size = self.sprite.get_size()
    
    def setScale(self, factors: Vector2f):
        self.sprite_transformed = pygame.transform.scale(self.sprite, (self.sprite_size[0] * factors[0], self.sprite_size[1] * factors[1]))
        self.sprite = self.sprite_transformed
    
    def getScale(self):
        width = self.sprite.get_width() / self.sprite_size[0]
        height = self.sprite.get_height() / self.sprite_size[1]
        
        return (width, height)

    def get_size(self):
        return self.sprite.get_size()
    
    def tick(self, current_screen_size, og_screen_size):
        width = self.get_size()[0]
        height = self.get_size()[1]
        
        screen_width_scale = current_screen_size[0] / og_screen_size[0]
        screen_height_scale = current_screen_size[1] / og_screen_size[1]
        
        self.sprite_shown = pygame.transform.scale(self.sprite_shown, (width * screen_width_scale, height * screen_height_scale))
        
        if "PFML_DEBUG_MODE" not in os.environ:
            print(f"{self.sprite_shown.get_width()}, {self.sprite_shown.get_height()}")

class Sprite():
    def __new__(self, texture: texture):
        return BetterSprite([texture.image, (0, 0), texture.smoothingness])
