import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Racing AI")

clock = pygame.time.Clock()

car_x = 400
car_y = 300
car_acceleration = 80
car_friction = 1.5
car_velocity = pygame.Vector2(0, 0)
car_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
car_surface.fill((255, 0, 0))
car_angle = 0
car_turn_speed = 120

running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    direction = pygame.Vector2(0, 0)

    if keys[pygame.K_d]:
        car_angle -= car_turn_speed * dt

    if keys[pygame.K_a]:
        car_angle += car_turn_speed * dt

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
    rotated_car = pygame.transform.rotate(car_surface, car_angle)
    rotated_rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, rotated_rect)
    pygame.display.flip()
    
pygame.quit()