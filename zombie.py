import pygame
import random

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super(Zombie, self).__init__()
        self.image = pygame.image.load('resources/images/zombie/Zombie_0.png').convert_alpha()
        self.images = [pygame.image.load(f'resources/images/zombie/Zombie_{i}.png').convert_alpha() for i in range(22)]
        self.dieimages = [pygame.image.load(f'resources/images/zombie/ZombieDie_{i}.png').convert_alpha() for i in range(10)]
        self.attackimages = [pygame.image.load(f'resources/images/zombie/ZombieAttack_{i}.png').convert_alpha() for i in range(21)]
        self.rect = self.images[0].get_rect()
        self.rect.y = 25 + random.randrange(0, 5) * 100
        self.rect.x = 1000
        self.speed = 3
        self.energy = 4
        self.dietimes = 0
        self.ismeetwallnut = False
        self.isalive = True

    def update(self, index=0):
        """Update zombie animation and movement."""
        if self.energy > 0:
            self.image = self.images[index % len(self.images)]
            if self.rect.x > 250 and self.ismeetwallnut:
                self.image = self.attackimages[index % len(self.attackimages)]
            if self.rect.x > 250 and not self.ismeetwallnut:
                self.rect.x -= self.speed
        else:
            if self.dietimes < 20:
                self.image = self.dieimages[self.dietimes // 2]
                self.dietimes += 1
            elif self.dietimes > 30:
                self.isalive = False
                self.kill()
            else:
                self.dietimes += 1
