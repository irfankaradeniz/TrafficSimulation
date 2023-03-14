class Agent:
    def __init__(self, id, position, speed):
        self.id = id
        self.position = position
        self.speed = speed

    def move(self, environment):
        pass

class Car(Agent):
    def __init__(self, id, position, speed, road_id, lane, max_speed=33.3, acceleration=2.5):
        super().__init__(id, position, speed)
        self.road_id = road_id
        self.lane = lane
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.wait_counter = 0

    def move(self, environment):
        car_ahead = environment.get_car_ahead(self)
        intersection = environment.get_next_intersection(self.road_id, self.position)
        traffic_light = environment.get_traffic_light(intersection, self.road_id)

        if self.should_stop(intersection, traffic_light, car_ahead):
            print(f"Car {self.id} should stop")
            self.speed = max(0, self.speed - self.acceleration)
            self.wait_counter += 1
        else:
            if self.wait_counter >= 3:  # Check if the car has waited for at least 3 seconds
                self.speed = min(self.max_speed, self.speed + self.acceleration)
            elif self.speed == 0:  # If the car has stopped at the red light, start moving again when the light turns green
                self.speed = min(self.max_speed, self.speed + self.acceleration)
            else:
                self.speed = min(self.max_speed, self.speed)

            self.wait_counter = 0

        self.position += self.speed

        road_length = environment.get_road_length(self.road_id)
        if self.position >= road_length:
            self.position = 0
            self.speed = min(self.max_speed, self.speed)


    def should_stop(self, intersection, traffic_light, car_ahead):
        if intersection is None or traffic_light is None:
            print(f"Car {self.id} no intersection or traffic light")
            return False

        distance_to_intersection = intersection.position - self.position
        print(f"Car {self.id} distance_to_intersection: {distance_to_intersection}")

        # Check the traffic light state before checking the distance to the intersection
        if traffic_light.state == 0:
            red_light_ahead = 0 < distance_to_intersection <= self.speed + 10
        else:
            red_light_ahead = False
        print(f"Car {self.id} red_light_ahead: {red_light_ahead}")

        if car_ahead is not None:
            distance_to_car_ahead = car_ahead.position - self.position
            too_close_to_car_ahead = 0 < distance_to_car_ahead <= self.speed + 10
            print(f"Car {self.id} too_close_to_car_ahead: {too_close_to_car_ahead}")
        else:
            too_close_to_car_ahead = False
            print(f"Car {self.id} no car ahead")

        if red_light_ahead or too_close_to_car_ahead:
            print(f"Car {self.id} should stop")

        return red_light_ahead or too_close_to_car_ahead

class Pedestrian(Agent):
    def __init__(self, id, position, speed, road_id, walking_direction):
        super().__init__(id, position, speed)
        self.road_id = road_id
        self.walking_direction = walking_direction

    def move(self, environment):
        self.position += self.speed * self.walking_direction
        road_length = environment.get_road_length(self.road_id)

        if self.position < 0 or self.position >= road_length:
            self.walking_direction *= -1