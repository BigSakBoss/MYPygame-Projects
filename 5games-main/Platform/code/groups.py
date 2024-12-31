
from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2()

    def draw(self, player_pos):
        
        self.offset.x = -(player_pos.centerx - WINDOW_WIDTH/2)
        self.offset.y = -(player_pos.centery - WINDOW_HEIGHT/2)

        # self.ground_sprites = [sprite for sprite in self if hasattr(sprite, "ground")]
        # self._sprites = [sprite for sprite in self if hasattr(sprite, "ground")]

        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)