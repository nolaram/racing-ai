import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Racing AI")

clock = pygame.time.Clock()

car_x = 400
car_y = 300
car_acceleration = 400
car_friction = 1.0
car_velocity = pygame.Vector2(0, 0)
car_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
car_surface.fill((255, 0, 0))
car_angle = 0
car_turn_speed = 120
car_max_speed = 200
car_normal_grip = 5.0
car_drift_grip = 0.5

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

    angle_rad = math.radians(car_angle)
    forward = pygame.Vector2(
        -math.sin(angle_rad),
        -math.cos(angle_rad)
    )
    
    if keys[pygame.K_w]:
        direction += forward

    if keys[pygame.K_s]:
        direction -= forward

    if keys[pygame.K_SPACE]:
        car_lateral_grip = car_drift_grip
    else:
        car_lateral_grip = car_normal_grip

    if direction.length() > 0:
        direction = direction.normalize()

    car_velocity += direction * car_acceleration * dt
    car_velocity *= math.exp(-car_friction * dt)
    speed = car_velocity.length()
    if speed > car_max_speed:
        car_velocity = car_velocity.normalize() * car_max_speed
    forward_speed = car_velocity.dot(forward)
    longitudinal_velocity = forward * forward_speed
    lateral_velocity = car_velocity - longitudinal_velocity
    lateral_damping = math.exp(-car_lateral_grip * dt)
    car_velocity = longitudinal_velocity + lateral_velocity * lateral_damping
    car_x += car_velocity.x * dt
    car_y += car_velocity.y * dt

    screen.fill((0, 0, 0))
    rotated_car = pygame.transform.rotate(car_surface, car_angle)
    rotated_rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, rotated_rect)
    pygame.display.flip()
    
pygame.quit()