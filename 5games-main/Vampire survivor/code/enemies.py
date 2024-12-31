from settings import*
from random import choice

class Enemies(pygame.sprite.Sprite):
    def __init__(self, pos, player, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.randomise_surf()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.frame_index = 0

        #movement
        self.speed = 200
        self.direction = Vector2(1,0)
        self.player = player

        #timer
        self.death_time = 0
        self.death_duration = 300

    def load_images(self):
        self.enemies_dict = {"bat": [], "blob": [], "skeleton":[]}
        
        for enemy in self.enemies_dict:
            
            for folder_path, subfolders, file_names in walk("5games-main/Vampire survivor/images/enemies/" + f"{enemy}"):
                if file_names: 
                    for file in file_names:
                        surf = pygame.image.load(join(folder_path , file))
                        self.enemies_dict[enemy].append(surf)
    

    def randomise_surf(self):

        self.key = choice(list(self.enemies_dict.keys()))
        self.image = self.enemies_dict[self.key][0]


    def get_direction(self):
        self.direction_x = self.player.rect.centerx - self.rect.centerx
        self.direction_y = self.player.rect.centery - self.rect.centery
        self.direction = Vector2(self.direction_x, self.direction_y).normalize() if self.direction.magnitude() else self.direction


    def move(self, dt):
        self.get_direction()
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center


    def collision(self, direction):
        for obstacle in self.collision_sprites:
            if self.hitbox_rect.colliderect(obstacle.rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.hitbox_rect.right = obstacle.rect.left
                    elif self.direction.x < 0: self.hitbox_rect.left = obstacle.rect.right
                elif direction == "vertical":
                    if self.direction.y > 0: self.hitbox_rect.bottom = obstacle.rect.top
                    elif self.direction.y < 0: self.hitbox_rect.top = obstacle.rect.bottom

    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        surf = pygame.mask.from_surface(self.enemies_dict[self.key][0]).to_surface()
        surf.set_colorkey("black")
        self.image = surf
       
    def check_timer(self):
            if pygame.time.get_ticks() - self.death_time > self.death_duration:
                self.kill()

    def animate(self, dt):
        
        self.frame_index += 5 * dt if self.direction else 0
        self.image = self.enemies_dict[self.key][int(self.frame_index) % len(self.enemies_dict[self.key])]


    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else: 
            self.check_timer()
        






