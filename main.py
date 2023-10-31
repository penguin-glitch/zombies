import pygame, math, random

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def dist(p1, p2):
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    return math.sqrt((dx*dx) + (dy*dy))

def run():

    def draw():
        screen.fill((50, 200, 50))
        for effect in effects:
            effect.draw(screen)
        sprites.draw(screen)
        pygame.display.flip()

    def handle_events(events):
        for event in events:
            if event.type == pygame.QUIT:
                return True
                
    
    sprites = pygame.sprite.Group()
    effects = pygame.sprite.Group()

    test_zombies = [Zombie(400, 300), Zombie(350, 300), Zombie(400, 320), Zombie(400, 290)]
    test_humans = [Human(200, 100), Human(700, 400), Human(100, 300)]
    sprites.add(test_zombies)
    sprites.add(test_humans)

    done = False
    dt = 0
    while not done:
        done = handle_events(pygame.event.get())

        sprites.update(dt, sprites, effects)
        effects.update(dt)

        draw()

        dt = clock.tick(60)

    pygame.quit()

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        self.image.convert_alpha()

        self.rect = pygame.Rect(x-12, y-12, 24, 24)
        self.x, self.y = x, y

        self.goal = None
        self.cooldown = 0
    
    def move(self, goal:tuple, speed:float):
        if dist(self.rect.center, goal) <= 24:
            return True

        # calc angle
        dx = self.x - goal[0]
        dy = self.y - goal[1]
        try:
            angle = math.atan((abs(dy)/abs(dx)))
        except ZeroDivisionError:
            angle = math.pi / 2

        self.x += math.cos(angle) * speed * -(dx/abs(dx))
        self.y += math.sin(angle) * speed * -(dy/abs(dy))
        self.rect.center = (self.x, self.y)

        return False

    def seek(self, sprites, goal):
        closest = None
        for sprite in [sprite for sprite in sprites if dist(self.rect.center, sprite.rect.center) < self.range]:
            if isinstance(sprite, goal):
                if closest == None or dist(self.rect.center, sprite.rect.center) < dist(self.rect.center, closest.rect.center):
                    closest = sprite
        return closest

    def take_damage(self, attacker):
        self.health -= attacker.damage
        try:
            range_mod = (attacker.range / dist(self.rect.center, attacker.rect.center) - 1)
        except ZeroDivisionError:
            range_mod = 1.9
        if random.randint(1,100) < (attacker.accuracy * range_mod) or self.health < 0:
            self.kill()

class Zombie(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.circle(self.image, (50, 100, 50), (12, 12), 12)
        self.range = 300
        self.health = 4
        self.damage = 2

    def update(self, dt, sprites, effects):
        if self.cooldown <= 0:
            self.goal = self.seek(sprites, Human)
            self.cooldown = 1000
        else: self.cooldown -= dt

        if self.goal != None:
            if self.move(self.goal.rect.center, 1):
                self.goal.kill()
                sprites.add(Zombie(self.goal.x, self.goal.y))
                self.goal = self.seek(sprites, Human)

class Human(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.circle(self.image, (191, 144, 90), (12, 12), 12)

        self.damage = 1
        self.health = 5
        self.range = 300
        self.accuracy = 50

    def update(self, dt, sprites, effects):
        if self.cooldown > 0:
            self.cooldown -= dt
        else:
            self.fire(sprites, effects)

    def fire(self, sprites, effects):

        # Find all targets within range that arent obstructed
        targets = []
        for sprite in [x for x in sprites if dist(x.rect.center, self.rect.center) < self.range]:
            if isinstance(sprite, Zombie):
                line = (self.x, self.y, sprite.x, sprite.y)
                blocked = False
                for obstacle in sprites:
                    if obstacle is not sprite and obstacle is not self:
                        if obstacle.rect.clipline(line):
                            blocked = True
                            break
                if not blocked:
                    targets.append(sprite)

        # Find closest target
        target = self.seek(targets, Zombie)

        if target is not None:
            target.take_damage(self)
            self.cooldown = 1000
            effects.add(Effect(pygame.draw.line, 100, [(255,255,0), self.rect.center, target.rect.center, 1]))
            
class Effect(pygame.sprite.Sprite):
    def __init__(self, base, duration, args):
        self.duration = duration
        self.args = args
        self.base = base
        super().__init__()

    def draw(self, screen):
        self.base(screen, *self.args)

    def update(self, dt):
        self.duration -= dt
        if self.duration < 0:
            self.kill()

run()