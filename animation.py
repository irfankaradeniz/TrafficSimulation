import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import pygame
import os

from agents import *

def visualize_environment(environment, agents, screen, road_texture, intersection_texture, car_texture, pedestrian_texture):
    if screen is None:
        return

    screen.fill((255, 255, 255))

    scale_factor = 7

    # Resize images
    road_texture = pygame.transform.scale(road_texture, (environment.roads[1].length * scale_factor, 10 * scale_factor))
    intersection_texture = pygame.transform.scale(intersection_texture, (10 * scale_factor, 30 * scale_factor))
    car_texture = pygame.transform.scale(car_texture, (15 * scale_factor, 15 * scale_factor))
    pedestrian_texture = pygame.transform.scale(pedestrian_texture, (15 * scale_factor, 15 * scale_factor))

    # Draw roads
    for road in environment.roads.values():
        screen.blit(road_texture, (0, road.id * 10 * scale_factor))

    # Draw intersections
    for intersection in environment.intersections.values():
        screen.blit(intersection_texture, (intersection.position * scale_factor, 0))

    # Draw traffic lights
    for intersection in environment.intersections.values():
        for traffic_light in intersection.traffic_lights:
            car_light_color = (255, 0, 0) if traffic_light.car_light_state == 0 else (0, 255, 0)
            pedestrian_light_color = (255, 0, 0) if traffic_light.pedestrian_light_state == 0 else (0, 255, 0)
            pygame.draw.circle(screen, car_light_color, (intersection.position * scale_factor + 5 * scale_factor, traffic_light.road_id * 10 * scale_factor + 5 * scale_factor), 2 * scale_factor)
            pygame.draw.circle(screen, pedestrian_light_color, (intersection.position * scale_factor + 5 * scale_factor, traffic_light.road_id * 10 * scale_factor + 8 * scale_factor), 2 * scale_factor)

    # Draw agents
    for agent in agents:
        if isinstance(agent, Car):
            car_rect = pygame.Rect(agent.position * scale_factor, agent.road_id * 20 * scale_factor + 2 * scale_factor, 15 * scale_factor, 15 * scale_factor)
            screen.blit(car_texture, car_rect)
        elif isinstance(agent, Pedestrian):
            pedestrian_rect = pedestrian_texture.get_rect(center=(int(agent.position * scale_factor), agent.road_id * 20 * scale_factor + 15 * scale_factor))
            screen.blit(pedestrian_texture, pedestrian_rect)

    pygame.display.update()



def animate(environment, agents, intersections, traffic_lights, simulation_steps, scale_factor=2):
    road_texture = pygame.image.load(os.path.join("textures", "road2.jpg"))
    intersection_texture = pygame.image.load(os.path.join("textures", "crosswalk.jpg"))
    car_texture = pygame.image.load(os.path.join("textures", "car1.png"))
    pedestrian_texture = pygame.image.load(os.path.join("textures", "walk.png"))
    pygame.init()
    screen_width = (max(road.length for road in environment.roads.values()) + 100) * scale_factor
    screen_height = (max(environment.roads.keys()) + 1) * 20 * scale_factor
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Traffic Simulation")

    clock = pygame.time.Clock()

    for i in range(simulation_steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        environment.step()

        visualize_environment(environment, agents, screen, road_texture, intersection_texture, car_texture, pedestrian_texture)
        clock.tick(5)

    pygame.quit()