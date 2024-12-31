from settings import *
from math import atan2, degrees

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True


class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
    
        self.player = player
        self.distance = 140
        self.player_direction = Vector2(1,0)
        self.groups = groups
        #sprite setup
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join("5games-main/Vampire survivor/images/gun/gun.png")).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = (self.player.rect.center + self.distance*self.player_direction))
        self.flip = True
        

    def get_direction(self):
        mouse_pos = Vector2(pygame.mouse.get_pos()) 
        player_pos = Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.player_direction = (mouse_pos - player_pos).normalize() if mouse_pos != player_pos else self.player_direction
    

    def rotate_gun(self):
        angle = atan2(self.player_direction.y, self.player_direction.x)
        angle = -degrees(angle)
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, -angle, 1)    
            self.image = pygame.transform.flip(self.image, False, True)
       

    # def fire_gun(self):
    #     if pygame.mouse.get_just_pressed()[0]:
    #         if self.player_direction.x > 0: pos = self.rect.midright
    #         else: pos = self.rect.midleft

    #         Bullet(pos, self.player_direction, self.groups)
            


    def update(self, dt):
        self.get_direction()
        self.rotate_gun()
        # self.fire_gun()
        self.rect.center = self.player.rect.center + self.distance*self.player_direction
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups, player_rect):
        self.speed = 1000
        self.direction = direction
        self.pos = pos
        self.player_pos = player_rect

        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = self.pos)
       
    
    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        self.check_kill_bullet()
        
    def check_kill_bullet(self):
        if abs(self.rect.right - self.player_pos.centerx) > WINDOW_WIDTH/2 + 100:  self.kill()
        elif abs(self.rect.bottom - self.player_pos.centery) > WINDOW_HEIGHT/2 + 100:  self.kill()

        

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)