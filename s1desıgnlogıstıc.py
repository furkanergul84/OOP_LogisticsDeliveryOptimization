from abc import ABC, abstractmethod

# Base Classes ------------------------------------------------------

class LogisticsObject(ABC):
    def __init__(self, name, location=(0, 0)):
        self.name = name
        self.location = location

    @abstractmethod
    def move(self, direction):
        pass

    @abstractmethod
    def attack(self, target):
        """
        Logistics context:
        'attack' = service / delivery operation
        """
        pass


# Composition Classes -------------------------------------------------

class Vehicle:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

class CargoManager:
    def __init__(self):
        self.cargos = []

    def add(self, cargo):
        self.cargos.append(cargo)


# Main System Actors --------------------------------------------------

class DeliveryAgent(LogisticsObject):
    def __init__(self, name, efficiency=100, location=(0, 0)):
        super().__init__(name, location)
        self.efficiency = efficiency
        self.cargo_manager = CargoManager()
        self.vehicle = None

    def move(self, direction):
        x, y = self.location
        if direction == "north":
            self.location = (x, y - 1)
        elif direction == "south":
            self.location = (x, y + 1)
        elif direction == "west":
            self.location = (x - 1, y)
        elif direction == "east":
            self.location = (x + 1, y)

    def attack(self, target):
        delivery_power = self.vehicle.capacity if self.vehicle else 10
        target.service_level -= delivery_power
        print(f"{self.name} delivered to {target.name} with efficiency {delivery_power}.")


# Optimization / External Actors --------------------------------------

class DistributionCenter(LogisticsObject):
    def __init__(self, name, service_level=50, location=(0, 0), vehicle=None):
        super().__init__(name, location)
        self.service_level = service_level
        self.vehicle = vehicle

    @classmethod
    def from_preset(cls, preset_name):
        presets = {
            "urban": {"service_level": 40, "vehicle": Vehicle("Van", 20)},
            "industrial": {"service_level": 70, "vehicle": Vehicle("Truck", 35)}
        }
        data = presets.get(preset_name, {"service_level": 30, "vehicle": None})
        return cls(preset_name.capitalize(), data["service_level"], (0, 0), data["vehicle"])

    def move(self, direction):
        x, y = self.location
        if direction == "expand":
            self.location = (x + 1, y)

    def attack(self, target):
        service_effect = self.vehicle.capacity if self.vehicle else 5
        target.efficiency -= service_effect
        print(f"{self.name} optimized {target.name} by {service_effect} units.")


# Cargo / Item Classes -------------------------------------------------

class Cargo(LogisticsObject):
    def __init__(self, name, priority, location=(0, 0)):
        super().__init__(name, location)
        self.priority = priority

    def move(self, direction):
        pass  # Cargo does not move autonomously

    def attack(self, target):
        pass  # Cargo does not perform operations


# End of Logistics and Delivery Optimization System
