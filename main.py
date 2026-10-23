import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Racing AI")

clock = pygame.time.Clock()

car_x = 380
car_y = 270
car_acceleration = 80
car_friction = 1.5
car_velocity = pygame.Vector2(0, 0)

running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    direction = pygame.Vector2(0, 0)

    if keys[pygame.K_d]:
        direction.x += 1

    if keys[pygame.K_a]:
        direction.x -= 1

    if keys[pygame.K_w]:
        direction.y -= 1

    if keys[pygame.K_s]:
        direction.y += 1

    if direction.length() > 0:
        direction = direction.normalize()

    car_velocity += direction * car_acceleration * dt
    car_velocity *= math.exp(-car_friction * dt)
    car_x += car_velocity.x * dt
    car_y += car_velocity.y * dt

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (car_x, car_y, 40, 60))
    pygame.display.flip()
    
pygame.quit()