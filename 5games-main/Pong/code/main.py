from settings import * 
from sys import exit
import json


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
    

    def draw(self):
        
        for sprite in self:
            for i in range(5):
                    self.display_surface.blit(sprite.shadow_surf, sprite.rect.topleft + Vector2(i,i))
            
        
        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self, size, pos, groups, paddle_sprites, update_score_method):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS["ball"], (SIZE["ball"][0] / 2, SIZE["ball"][1] / 2), SIZE["ball"][0] / 2)

        #shadow
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf, COLORS["ball shadow"], (SIZE["ball"][0] / 2, SIZE["ball"][1] / 2), SIZE["ball"][0] / 2)

        # self.image.fill(COLORS["ball"])
        self.rect = self.image.get_frect(center = pos)
        self.oldrect = self.rect.copy()
        self.direction = Vector2(choice((1,-1)), uniform(0.7, 0.8) * choice((1,-1)))
        self.speed = SPEED["ball"]
        self.paddle_sprites = paddle_sprites

        self.death_time = 10
        self.update_score = update_score_method
        self.cooldown_duration = 1700
    
    
    def move(self, dt):
    

        self.rect.x += self.direction.x * self.speed * dt
        self.paddle_collision("horizontal")
        self.rect.y += self.direction.y * self.speed * dt
        self.paddle_collision("vertical")

        self.wall_collision()
    
    def reset(self):
        self.death_time = pygame.time.get_ticks()
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.cooldown()

    def cooldown(self):
        keys = pygame.key.get_pressed()
        if pygame.time.get_ticks() - self.death_time > self.cooldown_duration or keys[pygame.K_SPACE]:
            self.death_time = 0

    def wall_collision(self):
           
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:  
            self.update_score("player" if self.rect.x < WINDOW_WIDTH / 2 else "opponent")
            self.reset()

       
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom >= WINDOW_HEIGHT else self.rect.bottom
        self.rect.top = 0 if self.rect.top <= 0 else self.rect.top
        if self.rect.bottom == WINDOW_HEIGHT or self.rect.top == 0: self.direction.y *= -1

    def paddle_collision(self, direction):

        for paddle in self.paddle_sprites:
            if self.rect.colliderect(paddle):
                if direction == "horizontal":
                    if self.rect.right >= paddle.rect.left and self.oldrect.right <= paddle.oldrect.left:
                            self.rect.right = paddle.rect.left
                            self.direction.x *= -1

                    if self.rect.left <= paddle.rect.right and self.oldrect.left >= paddle.oldrect.right:
                            self.rect.left = paddle.rect.right
                            self.direction.x *= -1

                
                elif direction == "vertical":
                    if self.rect.bottom >= paddle.rect.top and self.oldrect.bottom <= paddle.oldrect.top:
                            self.rect.bottom = paddle.rect.top
                            self.direction.y *= -1


                    if self.rect.top <= paddle.rect.bottom and self.oldrect.top > paddle.oldrect.bottom:
                            self.rect.top = paddle.rect.bottom
                            self.direction.y *= -1
    
    def update(self, dt):
        self.oldrect = self.rect.copy()
        
        if self.death_time == 0: self.move(dt)
        else: self.cooldown()


class Paddle(pygame.sprite.Sprite):
     def __init__(self, size, pos, colour, speed, groups):
        super().__init__(groups)

        #image
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(self.image, colour, pygame.FRect((0,0), SIZE["paddle"]), 0, 7)

        #shadow
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf, COLORS["paddle shadow"], pygame.FRect((0,0), SIZE["paddle"]), 0, 7)

        self.rect = self.image.get_frect(center = pos)
        self.oldrect = self.rect.copy()
        
        #movement
        self.direction = Vector2()
        self.limit = 40
     
     def update(self, dt):
        self.input_direction()
        
        self.oldrect = self.rect.copy()
        self.rect.centery += self.direction.y * self.speed * dt

        self.limit_movement()


     def limit_movement(self):    
        self.rect.top = self.limit if self.rect.top < self.limit else self.rect.top       
        self.rect.bottom = WINDOW_HEIGHT - self.limit if self.rect.bottom > WINDOW_HEIGHT - self.limit else self.rect.bottom 


class Player(Paddle):
    def __init__(self, size, pos, colour, speed, groups):
         super().__init__(size, pos, colour, speed, groups)
         self.speed = speed
    
    def input_direction(self):
        
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])


class Opponent(Paddle):
     def __init__(self, size, pos, colour, speed, groups, ball):
        super().__init__(size, pos, colour, speed, groups)
       
        self.speed = speed
        self.ball = ball
    
     def input_direction(self):
        
         self.direction.y = 1 if self.rect.centery < self.ball.rect.centery else -1
    


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        # sprite setup
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        self.setup()

        #score setup
        # try:
        #     with open("5games-main/Pong/code/data/score.txt") as score_file:
        #         self.score = json.load(score_file)
        # except:
        self.score = {"player": 0, "opponent": 0}
       
        self.font = pygame.font.Font(None, 160)


    def setup(self):
        self.ball_sprite = Ball(SIZE["ball"], (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), self.all_sprites, self.paddle_sprites, self.update_score)
        self.player = Player(SIZE["paddle"], POS["player"], COLORS["paddle"], SPEED["player"], (self.all_sprites, self.paddle_sprites))
        self.opponent = Opponent(SIZE["paddle"], POS["opponent"], COLORS["paddle"], SPEED["opponent"], (self.all_sprites, self.paddle_sprites), self.ball_sprite)
        

    def display_score(self):
        #player
        player_score_surf = self.font.render(str(self.score["player"]), True, COLORS["bg detail"])
        player_score_rect = player_score_surf.get_frect(center = (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2))
        self.screen.blit(player_score_surf, player_score_rect)

        #opponent
        opponent_score_surf = self.font.render(str(self.score["opponent"]), True, COLORS["bg detail"])
        opponent_score_rect = opponent_score_surf.get_frect(center = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
        self.screen.blit(opponent_score_surf, opponent_score_rect)

        #line seperator
        pygame.draw.line(self.screen, COLORS["bg detail"], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 6)
    
    def update_score(self, side):
        self.score["player" if side == "player" else "opponent"] += 1
        


    
    def update(self):
        self.display_score()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    with open("5games-main/Pong/code/data/score.txt", "w") as score_file:
                        json.dump(self.score, score_file)
            
            
            self.all_sprites.update(dt)
            self.screen.fill(COLORS["bg"])
            self.update()
            self.all_sprites.draw()

            pygame.display.update()


        pygame.quit()
        exit()


if __name__ == "__main__":
    game = Game()
    game.run()