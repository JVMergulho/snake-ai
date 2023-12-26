import pygame

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Buttom:
    def __init__(self, display, x, y, width, height, color):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(x,y, width, height)
        self.display = display
        self.color = color
        self.text = None

    def _is_pressed(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos) and (pygame.mouse.get_pressed()[0] == 1)
    
    def draw(self):
        pygame.draw.rect(self.display, self.color, self.rect, 0, 10)
        if not self.text is None:
            self.write(self.text, self.text_color)
        return self._is_pressed()
    
    def write(self, text, text_color):
        self.text = text
        self.text_color = text_color
        surface_text = font.render(text, True, text_color)
        self.display.blit(surface_text, [self.x + 10, self.y + 10])

