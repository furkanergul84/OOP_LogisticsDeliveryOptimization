from abc import ABC, abstractmethod
import random

# ================= BASE ABSTRACT CLASS =================

class LogisticsObject(ABC):
    def __init__(self, name, location=(0, 0)):
        self.name = name
        self.location = location

    @abstractmethod
    def move(self, direction):
        pass


# ================= CORE ENTITY =================

class LogisticsEntity(LogisticsObject):
    def __init__(self, name, status=100, location=(0, 0)):
        super().__init__(name, location)
        self._status = status
        self.active = True

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = max(0, value)
        if self._status == 0:
            self.active = False


# ================= CAPABILITY =================

class Capability:
    def __init__(self, name, efficiency):
        self.name = name
        self.efficiency = efficiency


# ================= STRATEGY (ALGORITHMIC DECISION) =================

class ResolutionStrategy(ABC):
    @abstractmethod
    def resolve(self, vehicle, issue):
        pass


class AggressiveStrategy(ResolutionStrategy):
    def resolve(self, vehicle, issue):
        power = vehicle.capability.efficiency + 5
        issue.status -= power
        vehicle.status -= 5
        print(f"[AGGRESSIVE] {vehicle.name} resolved {issue.name} (-{power})")


class SafeStrategy(ResolutionStrategy):
    def resolve(self, vehicle, issue):
        power = vehicle.capability.efficiency
        issue.status -= power
        print(f"[SAFE] {vehicle.name} resolved {issue.name} (-{power})")


# ================= VEHICLE =================

class Vehicle(LogisticsEntity):
    def __init__(self, name, status=100, location=(0, 0)):
        super().__init__(name, status, location)
        self.capability = None
        self.strategy = SafeStrategy()

    def move(self, direction):
        x, y = self.location
        if direction == "east":
            self.location = (x + 1, y)

    def choose_strategy(self):
        # Algorithmic decision
        if self.status < 40:
            self.strategy = SafeStrategy()
        else:
            self.strategy = AggressiveStrategy()

    def process_issue(self, issue):
        self.choose_strategy()
        self.strategy.resolve(self, issue)


# ================= ISSUE =================

class LogisticsIssue(LogisticsEntity):
    def __init__(self, name, severity=40, location=(0, 0)):
        super().__init__(name, severity, location)
        self.initial_severity = severity

    def move(self, direction):
        if direction == "spread":
            x, y = self.location
            self.location = (x + 1, y)


# ================= ADVANCED ENGINE =================

class LogisticsEngine:
    def __init__(self, vehicles, issues):
        self.vehicles = vehicles
        self.issues = issues
        self.turn = 0
        self.score = 0

    def random_event(self, vehicle):
        # Stochastic algorithm
        if random.randint(1, 10) > 8:
            vehicle.status -= 10
            print(f"[EVENT] Unexpected breakdown on {vehicle.name}")

    def step(self):
        self.turn += 1
        print(f"\n=== TURN {self.turn} ===")

        # Issues prioritized by severity
        self.issues.sort(key=lambda i: i.status, reverse=True)

        for vehicle in self.vehicles:
            if not vehicle.active:
                continue

            vehicle.move("east")
            self.random_event(vehicle)

            for issue in self.issues:
                if issue.active and issue.location == vehicle.location:
                    vehicle.process_issue(issue)

                    if not issue.active:
                        self.score += issue.initial_severity * 2
                        print(f"[RESOLVED] {issue.name} resolved (+score)")

        self.issues = [i for i in self.issues if i.active]

    def summary(self):
        print("\n=== OPERATION SUMMARY ===")
        print(f"Total Turns      : {self.turn}")
        print(f"Performance Score: {self.score}")


# ================= DEMO =================

def main():
    truck = Vehicle("Delivery Truck", location=(0, 0))
    truck.capability = Capability("Advanced Maintenance Kit", 12)

    delay = LogisticsIssue("Delay", severity=30, location=(1, 0))
    breakdown = LogisticsIssue("Breakdown", severity=60, location=(2, 0))

    engine = LogisticsEngine(
        vehicles=[truck],
        issues=[delay, breakdown]
    )

    for _ in range(5):
        if not truck.active:
            print("Vehicle out of service. Operation failed.")
            break
        engine.step()

    engine.summary()


if __name__ == "__main__":
    main()
