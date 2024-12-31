from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = Vector2()
    
    def draw(self, player_pos):
        self.offset.x = -(player_pos[0] - WINDOW_WIDTH/2)
        self.offset.y = -(player_pos[1] - WINDOW_HEIGHT/2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, "ground")]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, "ground")]
        

        for sprite in ground_sprites:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
            
        for sprite in sorted(object_sprites, key = lambda sprite: sprite.rect.centery):
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)