import pygame, math

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def run():

    def draw():
        screen.fill((50, 200, 50))
        sprites.draw(screen)
        pygame.display.flip()

    def handle_events(events):
        for event in events:
            if event.type == pygame.QUIT:
                return True
    
    sprites = pygame.sprite.Group()
    test_zomb = Zombie(400, 300)
    sprites.add(test_zomb)

    done = False
    while not done:
        done = handle_events(pygame.event.get())
        draw()

    pygame.quit()

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image.convert_alpha()

        self.rect = pygame.Rect(x, y, 24, 24)
        self.x, self.y = x, y
    
    def move(self, goal:tuple, speed:float):
        # calc angle
        dx = self.x - goal[0]
        dy = self.y - goal[1]
        angle = math.atan((dy/dx))

        self.x += math.cos(angle) * speed
        self.y += math.sin(angle) * speed
        self.rect.x, self.rect.y = self.x,self.y

    def seek(self)

class Zombie(Entity):
    def __init__(self, x, y):
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (50, 100, 50), (12, 12), 12)
        super().__init__(x, y)

run()