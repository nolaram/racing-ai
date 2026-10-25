import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Racing AI")

clock = pygame.time.Clock()

car_x = 300
car_y = 100
car_start_x = 300
car_start_y = 100
car_start_angle = 0
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
car_steering_reference_speed = 100
car_road_friction = 1.0
car_grass_friction = 3.0

outer_track = pygame.Rect(50,50, 700, 500)
inner_track = pygame.Rect(200, 150, 400, 300)

episode = 1
episode_time = 0.0

# checkpoint_1 = pygame.Rect(370, 50, 60, 100)
# checkpoint_1_completed = False
checkpoints = [
    pygame.Rect(370, 50, 60, 100),
    pygame.Rect(600, 270, 150, 60),
    pygame.Rect(370, 450, 60, 100),
    pygame.Rect(50, 270, 150, 60)
]
was_inside_checkpoint = False
current_checkpoint = 0
laps_completed = 0

running = True

while running:
    dt = clock.tick(60) / 1000.0
    episode_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    direction = pygame.Vector2(0, 0)
    speed = car_velocity.length()
    steering_factor = min(speed / car_steering_reference_speed, 1.0)

    angle_rad = math.radians(car_angle)

    forward_before_steering = pygame.Vector2(
        -math.sin(angle_rad),
        -math.cos(angle_rad)
    )

    signed_speed = car_velocity.dot(forward_before_steering)

    if signed_speed > 0:
        steering_direction = 1
    elif signed_speed < 0:
        steering_direction = -1
    else:
        steering_direction = 0

    if keys[pygame.K_d]:
        car_angle -= car_turn_speed * dt * steering_factor * steering_direction

    if keys[pygame.K_a]:
        car_angle += car_turn_speed * dt * steering_factor * steering_direction

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

    on_road = outer_track.collidepoint(car_x,car_y) and not inner_track.collidepoint(car_x,car_y)

    if on_road:
        terrain_multiplier = 1.0
        car_friction = car_road_friction
    else:
        terrain_multiplier = 0.4
        car_friction = car_grass_friction

    car_velocity += direction * car_acceleration * dt * terrain_multiplier
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

    on_road = outer_track.collidepoint(car_x,car_y) and not inner_track.collidepoint(car_x,car_y)

    if not on_road:
        car_x = car_start_x
        car_y = car_start_y
        car_angle = car_start_angle
        car_velocity = pygame.Vector2(0, 0)
        episode += 1
        print(f"Episode Time: {episode_time:.2f} seconds")
        episode_time = 0.0
        print(f"Episode: {episode}")

    if on_road:
        car_surface.fill((255, 0, 0))
    else:
        car_surface.fill((255, 255, 0))

    target_checkpoint = checkpoints[current_checkpoint]
    inside_target = target_checkpoint.collidepoint(car_x, car_y)
    if inside_target:
        print("Target checkpoint detected!")
        current_checkpoint += 1
        if current_checkpoint >= len(checkpoints):
            laps_completed += 1
            print(f"Lap completed! Laps: {laps_completed}")
            current_checkpoint = 0

    # inside_checkpoint = checkpoint_1.collidepoint(car_x, car_y)
    # if inside_checkpoint and not was_inside_checkpoint and not checkpoint_1_completed:
    #     print("Checkpoint 1 reached!")
    #     checkpoint_1_completed = True
    # was_inside_checkpoint = inside_checkpoint

    screen.fill((40, 110, 70))
    pygame.draw.rect(screen, (90, 90, 90), outer_track)
    pygame.draw.rect(screen, (40, 110, 70), inner_track)
    for checkpoint in checkpoints:
        pygame.draw.rect(screen, (255, 215, 0), checkpoint, 2)

    rotated_car = pygame.transform.rotate(car_surface, car_angle)
    rotated_rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, rotated_rect)
    pygame.display.flip()
    
pygame.quit()