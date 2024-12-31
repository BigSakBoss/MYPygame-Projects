from settings import *
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = "down", 0
        self.image = pygame.image.load("5games-main/Vampire survivor/images/player/down/0.png").convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hit_box_rect = self.rect.inflate(-58, -90)
        self.direction = Vector2 ()
        self.speed = 500
        self.collision_sprites = collision_sprites
    

    def load_images(self):
        self.frames = {"left": [], "right": [], "up": [], "down": []}

        for state in self.frames.keys():
            for folder_path, subfolder, file_names in walk("5games-main/Vampire survivor/images/player/" + f"{state}"):
                if file_names:
                    for file in sorted(file_names, key = lambda file: int(file[0])):
                        full_path = join(folder_path, file)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)
            

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s])- int(keys[pygame.K_UP] or keys[pygame.K_w])
        magnitude = self.direction.magnitude()
        if magnitude:
            self.direction *= 1/magnitude
        else: self.moving = False


    def move(self, dt):
        self.hit_box_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hit_box_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hit_box_rect.center


    def collision(self, direction):
        for obstacle in self.collision_sprites:
            if obstacle.rect.colliderect(self.hit_box_rect):
                if direction == "horizontal":
                    if self.direction.x > 0:  self.hit_box_rect.right = obstacle.rect.left
                    elif self.direction.x < 0:  self.hit_box_rect.left = obstacle.rect.right
                if direction == "vertical":
                    if self.direction.y > 0:  self.hit_box_rect.bottom = obstacle.rect.top
                    elif self.direction.y < 0:  self.hit_box_rect.top = obstacle.rect.bottom


    def animate(self, dt):

            if self.direction.x != 0: 
                self.state = "right" if self.direction.x > 0 else "left"
            if self.direction.y != 0:
                self.state = "down" if self.direction.y > 0 else "up"


            self.frame_index = self.frame_index + 5 * dt if self.direction else 0

            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]


    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
