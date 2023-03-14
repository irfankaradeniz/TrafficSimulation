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

    intersection = Intersection(1, 50, [road1.id], [road2.id], traffic_lights)  # Fix the connection between roads and the intersection
    environment.add_intersection(intersection)

    # Create agents
    car1 = Car(1, 0, 5, 1, 1, 33.3, 2.5)
    car2 = Car(2, 20, 5, 1, 1, 33.3, 2.5)
    pedestrian = Pedestrian(3, 0, 1, 1, 1)
    environment.add_agent(car1)
    environment.add_agent(car2)
    environment.add_agent(pedestrian)

    # Initialize the animation
    fig, ax = plt.subplots(figsize=(16, 9))

    # Run simulation
    simulation_steps = 100
    for _ in range(simulation_steps):
        environment.step()

        # Print agent positions and traffic light states for visualization purposes
        # print("Car 1 position:", car1.position)
        # print("Car 1 speed:", car1.speed)
        # print("Car 2 position:", car2.position)
        # print("Car 2 speed:", car2.speed)
        # print("Pedestrian position:", pedestrian.position)
        # print("Traffic light 1 state:", intersection.traffic_lights[0].state)
        # print("Traffic light 2 state:", intersection.traffic_lights[1].state)
        # print("----------")

        # Update the animation for the current step
        visualize_environment(environment, [car1, car2, pedestrian], fig, ax)
        plt.pause(0.1)

    plt.show()

if __name__ == "__main__":
    main()