import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

from agents import *

def visualize_environment(environment, agents, fig, ax):
    ax.clear()

    # Draw roads
    for road in environment.roads.values():
        ax.add_patch(patches.Rectangle((0, road.id * 10), road.length, 10, edgecolor="black", facecolor="gray"))

    # Draw intersections
    for intersection in environment.intersections.values():
        ax.add_patch(patches.Rectangle((intersection.position, 0), 10, 30, edgecolor="black", facecolor="white"))

    # Draw traffic lights
    for intersection in environment.intersections.values():
        for traffic_light in intersection.traffic_lights:
            color = "red" if traffic_light.state == 0 else "green"
            ax.add_patch(patches.Circle((intersection.position + 5, traffic_light.road_id * 10 + 5), 1, color=color))

    # Draw agents
    for agent in agents:
        if isinstance(agent, Car):
            ax.add_patch(patches.Rectangle((agent.position, agent.road_id * 10 + 2), 5, 5, edgecolor="black", facecolor="blue"))
        elif isinstance(agent, Pedestrian):
            ax.add_patch(patches.Circle((agent.position, agent.road_id * 10 + 7), 1, color="orange"))

    ax.set_xlim(0, max(road.length for road in environment.roads.values()))
    ax.set_ylim(0, (max(environment.roads.keys()) + 1) * 10)

def animate(environment, agents, intersections, traffic_lights, simulation_steps):
    fig, ax = plt.subplots(figsize=(16, 9))

    def update(step):
        environment.step()

        visualize_environment(environment, agents, fig, ax)
        plt.pause(0.1)

    anim = FuncAnimation(fig, update, frames=simulation_steps, interval=100, repeat=False)
    plt.show()