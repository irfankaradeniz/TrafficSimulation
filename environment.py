from agents import *
class Road:
    def __init__(self, id, length, lanes):
        self.id = id
        self.length = length
        self.lanes = lanes

class Intersection:
    def __init__(self, id, position, incoming_roads, outgoing_roads, traffic_lights):
        self.id = id
        self.position = position
        self.incoming_roads = incoming_roads
        self.outgoing_roads = outgoing_roads
        self.traffic_lights = traffic_lights

class TrafficLight:
    def __init__(self, id, road_id, lane, position, time_interval=10):
        self.id = id
        self.road_id = road_id
        self.lane = lane
        self.position = position
        self.time_interval = time_interval
        self.car_light_state = 1
        self.pedestrian_light_state = 0
        self.time_elapsed = 0

    def update(self):
        self.time_elapsed += 1
        if self.time_elapsed >= self.time_interval:
            self.car_light_state = (self.car_light_state + 1) % 2
            self.pedestrian_light_state = (self.pedestrian_light_state + 1) % 2
            self.time_elapsed = 0


class Environment:
    def __init__(self):
        self.roads = {}
        self.intersections = {}
        self.agents = {}

    def add_road(self, road):
        self.roads[road.id] = road

    def add_intersection(self, intersection):
        self.intersections[intersection.id] = intersection

    def add_agent(self, agent):
        self.agents[agent.id] = agent

    def get_road_length(self, road_id):
        return self.roads[road_id].length

    def step(self):
        for intersection in self.intersections.values():
            for traffic_light in intersection.traffic_lights:
                traffic_light.update()

        for agent in self.agents.values():
            agent.move(self)

    def get_car_ahead(self, car):
        cars_on_same_road_and_lane = [c for c in self.agents.values() if isinstance(c, Car) and c.road_id == car.road_id and c.lane == car.lane]
        cars_ahead = [c for c in cars_on_same_road_and_lane if c.position > car.position]
        return min(cars_ahead, key=lambda x: x.position) if cars_ahead else None

    def get_next_intersection(self, road_id, position):
        intersections_on_road = [i for i in self.intersections.values() if road_id in i.incoming_roads]
        intersections_ahead = [i for i in intersections_on_road if i.position >= position]
        next_intersection = min(intersections_ahead, key=lambda x: x.position) if intersections_ahead else None
        # if next_intersection is not None:
            # print(f"Next intersection for road {road_id}: {next_intersection.id}")
        return next_intersection

    def get_traffic_light(self, intersection, road_id):
        if intersection is None:
            return None

        traffic_light = next((tl for tl in intersection.traffic_lights if tl.road_id == road_id), None)
        # if traffic_light is not None:
            # print(f"Traffic light for intersection {intersection.id} and road {road_id}: {traffic_light.id}")
        return traffic_light