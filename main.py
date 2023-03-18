from agents import *
from environment import *
from animation import *

def main():

    environment = Environment()

    # Create roads
    road1 = Road(1, 200, 2)
    road2 = Road(2, 200, 2)
    environment.add_road(road1)
    environment.add_road(road2)

    # Create intersections
    traffic_light1 = TrafficLight(1, 1, 1, 50, 30)
    traffic_light2 = TrafficLight(2, 2, 1, 50, 30)
    traffic_lights = [traffic_light1, traffic_light2]

    intersection = Intersection(1, 50, [road1.id, road2.id], [road1.id, road2.id], traffic_lights)
    environment.add_intersection(intersection)

    # Create agents
    car1 = Car(1, 0, 5, 1, 1, 33.3, 2.5)
    car2 = Car(2, 20, 5, 1, 1, 33.3, 2.5)

    pedestrian = Pedestrian(3, 50, 1, 1, -1)
    environment.add_agent(car1)
    environment.add_agent(car2)
    environment.add_agent(pedestrian)

    # Initialize the animation
    animate(environment, [car1, car2, pedestrian], intersection, traffic_lights, simulation_steps=100, scale_factor=7)


if __name__ == "__main__":
    main()