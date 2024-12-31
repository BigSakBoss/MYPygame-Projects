from settings import *
from player import Player
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from enemies import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Survivor")
        self.clock = pygame.time.Clock()
        self.running = True
        self.can_shoot = True
        self.gun_cooldown = 100

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 800)
        self.enemy_positions = []
        self.enemies = 0
        
        self.setup()

        #audio
        self.shoot_sound = pygame.mixer.Sound("5games-main/Vampire survivor/audio/shoot.wav")
        self.shoot_sound.set_volume(0.4)
        self.impact_sound = pygame.mixer.Sound("5games-main/Vampire survivor/audio/impact.ogg")
        self.background_music = pygame.mixer.Sound("5games-main/Vampire survivor/audio/music.wav")
        self.background_music.set_volume(0.3)
        self.background_music.play(loops = -1)

        # sprites
        self.bullet = pygame.image.load("5games-main/Vampire survivor/images/gun/bullet.png").convert_alpha()
        

    def setup(self):
        map = load_pygame("5games-main/Vampire survivor/data/maps/world.tmx")
        
        for object in map.get_layer_by_name("Collisions"):
            width, height = object.width, object.height
            surf = pygame.Surface((width, height))
            CollisionSprite((object.x,object.y), surf, self.collision_sprites)

        for x ,y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), image, self.all_sprites)
        
        for object in map.get_layer_by_name("Objects"):
            CollisionSprite((object.x,object.y), object.image, (self.all_sprites, self.collision_sprites))
        
        for marker in map.get_layer_by_name("Entities"):
            if marker.name == "Player":
                self.player = Player((marker.x,marker.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.enemy_positions.append((marker.x, marker.y))
                

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + 55*(self.gun.player_direction).normalize()
            self.shoot_time = pygame.time.get_ticks()
            Bullet(self.bullet, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites), self.player.rect)   
            self.can_shoot = False 

        self.check_can_shoot()

    
    def check_can_shoot(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True


    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False
            


    def kill_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collisions = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collisions:
                    self.impact_sound.play()
                    for sprite in collisions:
                        time = pygame.time.get_ticks()
                        sprite.destroy()
                    bullet.kill()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemies(choice(self.enemy_positions), self.player, (self.all_sprites, self.enemy_sprites), self.collision_sprites)
                        
                
            # update
            self.update()
            self.all_sprites.update(dt)


            # draw
            self.screen.fill("black")
            self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()

        pygame.quit()
        exit()

            
    def update(self):
        self.input()
        self.kill_collision()
        self.player_collision()
        

if __name__ == "__main__":
    game = Game()
    game.run()