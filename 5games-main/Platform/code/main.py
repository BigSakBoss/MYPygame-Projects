from settings import * 
from sprites import *
from groups import *
from support import *
from cool import Timer


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True
        self.end_game = False
        self.end_game_timer = Timer(1500, func = self.stop_running)
        self.activated = False


        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.load_images()
        self.setup()

        # timers
        self.bee_timer = Timer(500, func= self.create_bee, repeat=True, autostart= True)


    def stop_running(self):
        self.running = False


    def create_bee(self):
        Bee(  pos  = ((self.level_width+ WINDOW_WIDTH), (randint(0, self.level_height))), 
            groups = (self.all_sprites, self.enemy_sprites), 
            frames = self.bee_frames, 
            speed  = randint(300,500))

    def create_bullet(self, pos, direction, flip = False):
        self.audio["shoot"].play()
        Bullet(pygame.transform.flip(self.bullet_surf, flip, False), pos, direction, (self.all_sprites, self.bullet_sprites))
        Fire(pygame.transform.flip(self.fire_surf, flip, False), pos, self.all_sprites, self.player)

    
    def collision(self):
        # bullets -> enemies
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                sprite_collisions = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if sprite_collisions:
                    self.audio["impact"].play()
                    bullet.kill()
                    for sprite in sprite_collisions:
                        sprite.destroy()
        
        # enemeies -> player
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask) and not self.end_game:
            self.audio["impact"].play()
            self.end_game = True
    

    def load_images(self):
        # graphics
        self.player_frames = import_folder("5games-main", "Platform", "images", "player")
        self.bullet_surf = import_image("5games-main", "Platform", "images", "gun", "bullet")
        self.fire_surf = import_image("5games-main", "Platform", "images", "gun", "fire")
        self.bee_frames = import_folder("5games-main", "Platform", "images", "enemies", "bee")
        self.worm_frames = import_folder("5games-main", "Platform", "images", "enemies", "worm")
       
        # sounds
        self.audio = audio_importer("5games-main", "Platform", "audio")
        print(self.audio)

    def setup(self):
        map = load_pygame("5games-main/Platform/data/maps/world.tmx")
        self.level_width, self.level_height = map.width * TILE_SIZE, map.height * TILE_SIZE


        for x, y, image in map.get_layer_by_name("Main").tiles():
            Sprite(image, (x*TILE_SIZE, y*TILE_SIZE), (self.all_sprites, self.collision_sprites))
            
        for x, y, image in map.get_layer_by_name("Decoration").tiles():
            Sprite(image, (x*TILE_SIZE, y*TILE_SIZE), self.all_sprites)

        for marker in map.get_layer_by_name("Entities"):
            if marker.name == "Player":
                self.player = Player((marker.x, marker.y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)
            elif marker.name == "Worm":
                Worm(pygame.FRect(marker.x, marker.y, marker.width, marker.height), (self.all_sprites, self.enemy_sprites), self.worm_frames)
        
        self.audio["music"].play(loops = -1)
        self.audio["music"].set_volume(0.24)
    
    def update(self):
        self.collision()
        self.end_game_timer.update()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.update()

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect)

            if not self.end_game:
                pygame.display.update()
            else:
                if not self.activated:
                    self.end_game_timer.activate()
                    self.activated = True
                
       

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 