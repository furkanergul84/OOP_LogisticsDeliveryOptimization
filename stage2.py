from abc import ABC, abstractmethod

# BASE ABSTRACT CLASS =====================================================

class LogisticsObject(ABC):
    def __init__(self, name, location=(0, 0)):
        self.name = name
        self.location = location

    @abstractmethod
    def move(self, direction):
        pass

    @abstractmethod
    def process(self, target):
        pass


# COMPOSITION CLASSES =====================================================

class Capability:
    def __init__(self, name, efficiency):
        self.name = name
        self.efficiency = efficiency  # problem solving power


class Cargo:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)


# COMMON ENTITY CLASS (Encapsulation) =====================================

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


# VEHICLE CLASS ===========================================================

class Vehicle(LogisticsEntity):
    def __init__(self, name, status=100, location=(0, 0)):
        super().__init__(name, status, location)
        self.cargo = Cargo()
        self.capability = None

    def move(self, direction):
        x, y = self.location
        routes = {
            "north": (x, y - 1),
            "south": (x, y + 1),
            "west": (x - 1, y),
            "east": (x + 1, y)
        }
        if direction in routes:
            self.location = routes[direction]

    def process(self, issue):
        efficiency = self.capability.efficiency if self.capability else 5
        issue.status -= efficiency
        print(f"{self.name} resolved {issue.name} (-{efficiency})")


# RISK / ISSUE CLASS ======================================================

class LogisticsIssue(LogisticsEntity):
    def __init__(self, name, status=40, location=(0, 0), impact=None):
        super().__init__(name, status, location)
        self.impact = impact

    @classmethod
    def from_type(cls, issue_type):
        presets = {
            "delay": {"status": 30, "impact": Capability("Time Loss", 6)},
            "breakdown": {"status": 60, "impact": Capability("Mechanical Risk", 10)}
        }
        data = presets.get(issue_type, {"status": 20, "impact": None})
        return cls(issue_type.capitalize(), data["status"], (0, 0), data["impact"])

    def move(self, direction):
        # Issues spread forward in the network
        x, y = self.location
        if direction == "spread":
            self.location = (x + 1, y)

    def process(self, vehicle):
        impact = self.impact.efficiency if self.impact else 4
        vehicle.status -= impact
        print(f"{self.name} affected {vehicle.name} (-{impact})")


# NETWORK MAP =============================================================

class LogisticsNetwork:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def is_inside(self, location):
        x, y = location
        return 0 <= x < self.width and 0 <= y < self.height

    def detect_conflicts(self, objects):
        positions = {}
        conflicts = []
        for obj in objects:
            if obj.location in positions:
                conflicts.append((obj, positions[obj.location]))
            else:
                positions[obj.location] = obj
        return conflicts


# LOGISTICS ENGINE (TURN-BASED) ===========================================

class LogisticsEngine:
    def __init__(self, network, vehicles, issues):
        self.network = network
        self.vehicles = vehicles
        self.issues = issues
        self.turn = 0

    def step(self):
        self.turn += 1
        print(f"\n--- OPERATION TURN {self.turn} ---")

        # Vehicles move
        for vehicle in self.vehicles:
            vehicle.move("east")

        # Issues spread
        for issue in self.issues:
            issue.move("spread")

        # Conflict resolution
        conflicts = self.network.detect_conflicts(self.vehicles + self.issues)
        for obj1, obj2 in conflicts:
            self.resolve(obj1, obj2)

        # Remove resolved issues
        self.issues = [i for i in self.issues if i.active]

    def resolve(self, obj1, obj2):
        if isinstance(obj1, Vehicle) and isinstance(obj2, LogisticsIssue):
            obj1.process(obj2)
            if obj2.active:
                obj2.process(obj1)

        elif isinstance(obj1, LogisticsIssue) and isinstance(obj2, Vehicle):
            obj2.process(obj1)
            if obj1.active:
                obj1.process(obj2)


# DEMO ===================================================================

def main():
    network = LogisticsNetwork(5, 5)

    truck = Vehicle("Delivery Truck", location=(0, 0))
    truck.capability = Capability("GPS & Maintenance Kit", 12)

    delay_issue = LogisticsIssue.from_type("delay")
    delay_issue.location = (1, 0)

    engine = LogisticsEngine(
        network=network,
        vehicles=[truck],
        issues=[delay_issue]
    )

    for _ in range(5):
        if not truck.active:
            print("Vehicle out of service. Operation failed.")
            break
        engine.step()

    print("\nLogistics operation finished.")


if __name__ == "__main__":
    main()
