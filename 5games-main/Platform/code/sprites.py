from settings import *
from cool import Timer
from math import sin

class Sprite(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 9
        super().__init__(self.frames[self.frame_index], pos, groups)
        self.ground = False

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.death_timer = Timer(200, func = self.kill)

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey("black")

    def update(self, dt):
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
        self.constraint()
        self.death_timer.update()

class Bee(Enemy):
    def __init__(self, pos, groups, frames, speed):
        super().__init__(frames, pos, groups)

        self.speed = speed
        self.initial_posy = pos[1]
        self.amplitude = randint(300,400)
        self.frequency = randint(300,600)

    
    def move(self, dt):
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt
    
    def constraint(self):
        if self.rect.right <= -500:
            self.kill()
    
class Worm(Enemy):
    def __init__(self, area_rect, groups, frames):
        self.area_rect = area_rect
        pos = self.area_rect.topleft + Vector2(0,35)
        super().__init__(frames, pos, groups)

        
        # movement
        self.speed = randint(70,130)
        self.direction = Vector2(1,0)
        self.right_constraint = self.area_rect.right
        self.left_constraint = self.area_rect.left
        self.flip = False

    
    def move(self, dt):
        self.rect.x += self.speed * self.direction.x * dt


    def constraint(self):
        if not self.area_rect.contains(self.rect): #self.rect.right >= self.right_constraint or self.rect.left <= self.left_constraint:
            self.direction.x *= -1
            # self.flip = not(self.flip)
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
 
class Bullet(Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(surf, pos, groups)

        
        self.direction = direction
        self.speed = 1000
    
    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

class Fire(Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(surf, pos, groups)

        self.timer = Timer(100, autostart=True, func = self.kill)
        self.player = player
        self.flip = player.flip
        self.offset_y = Vector2(0,8)

        self.check_timer()
    
    def check_timer(self):
        if self.timer: 
            if self.flip == self.player.flip:
                if not self.flip:
                    self.rect.midleft = self.player.rect.midright + self.offset_y 
                else:
                    self.rect.midright = self.player.rect.midleft + self.offset_y #self.player.rect.center + Vector2(33,-10) if not self.flip else self.player.rect.center + Vector2((-33 - self.image.get_width()), -10)
            
            else: self.kill()
    
    def update(self, dt):
        self.check_timer()
        self.timer.update()

class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames, create_bullet_method):
        super().__init__(frames, pos, groups)
        self.onfloor = False
        self.flip = False

        #movement
        self.direction = Vector2()
        self.speed = 400

        #collision sprites
        self.collision_sprites = collision_sprites

        # gravity
        self.gravity = 50

        # timer
        self.shoot_timer = Timer(300)

        self.create_bullet = create_bullet_method
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])

        if keys[pygame.K_w] and self.onfloor: 
            self.direction.y = -20
        
        mouse_buttons = pygame.mouse.get_pressed()
        
        if mouse_buttons[0] and not self.shoot_timer:
            pos = self.rect.midright if not self.flip else self.rect.midleft + Vector2(-47,0)
            self.create_bullet(pos, -1 if self.flip else 1, flip = self.flip)

            self.shoot_timer.activate()
    
    def move(self, dt):
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")

        # vertical 
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision("vertical")
    
    def collision(self, direction):
        for obstacle in self.collision_sprites:
            if obstacle.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.direction.x < 0: self.rect.left = obstacle.rect.right
                    elif self.rect.x > 0: self.rect.right = obstacle.rect.left
                elif direction == "vertical":
                    if self.direction.y > 0: self.rect.bottom = obstacle.rect.top
                    elif self.direction.y < 0: self.rect.top = obstacle.rect.bottom
                    self.direction.y = 0

    def check_floor(self):
        bottom_rect = pygame.FRect((0,0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collision_sprites]
        self.onfloor = True if bottom_rect.collidelist(level_rects) >= 0 else False

    def player_state_animation(self, dt):
        if self.direction.x: 
            self.animate(dt)
            self.flip = self.direction.x < 0
            self.image = pygame.transform.flip(self.image, self.flip, False)
        
        if not self.direction.x or not self.onfloor:
            state = self.onfloor == False
            self.image = pygame.transform.flip(self.frames[state], self.flip, False)
        

    def update(self, dt):

        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.player_state_animation(dt)
     