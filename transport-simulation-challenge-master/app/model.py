from dataclasses import dataclass, field
from math import sqrt
from typing import ClassVar

@dataclass
class Bus:
    STATUS_EN_RUTA: ClassVar[str] = "en ruta"
    STATUS_EN_TERMINAL: ClassVar[str] = "en la terminal"
    
    id: int
    route: str = field(default="")
    capacity: int = field(default=8)
    occupied_seats: int = field(default=0)
    status: str = field(init=False, default=STATUS_EN_TERMINAL)
    location: tuple[int, int] = field(init=False, default=(0,0))
    
    def assign_route(self, route: str):
        self.route = route
        
    def update_occupied_seats(self, occupied_seats: int):
        if occupied_seats >= 0 and occupied_seats <= self.capacity:
            self.occupied_seats = occupied_seats

    def toggle_status(self):
        if self.status == self.STATUS_EN_RUTA:
            self.status = self.STATUS_EN_TERMINAL
        else:
            self.status = self.STATUS_EN_RUTA
    
    def update_location(self, new_x: int, new_y: int):
        tupla = (new_x, new_y)
        self.location = tupla
    
    def calculate_distance(self, dest_x: int, dest_y: int) -> float:
        distancia = sqrt(((dest_x - self.location[0])**2) + ((dest_y - self.location[1])**2))
        return distancia
    
class TransportManager:
    def __init__(self, buses:dict[int, Bus] = {}):
        self.buses = buses
        
    def add_bus(self, capacity: int) -> int:
        bus_id = len(self.buses) + 1
        new_bus = Bus(id=bus_id, capacity=capacity)
        self.buses[bus_id] = new_bus
        return bus_id
    
    def assign_route(self, bus_id: int, route: str):
        self.buses[bus_id].route = route
    
    def buses_by_status(self, status: str) -> list[Bus]:
        lista_buses = [bus for bus in self.buses.values() if bus.status == status]
        return lista_buses        
    
    def buses_by_route(self, route: str) -> list[Bus]:
        lista_buses = [bus for bus in self.buses.values() if bus.route == route]
        return lista_buses  
    
    def update_bus_location(self, bus_id: int, new_x: int, new_y: int):
        for bus in self.buses.values():
            if bus.id == bus_id:
                bus.location = (new_x, new_y)
    
    def calculate_distance_to_destination(self, bus_id: int, destination_x: int, destination_y: int) -> float:
        for bus in self.buses.values():
            if bus.id == bus_id:
                return bus.calculate_distance(destination_x, destination_y)
            else:
                return -1
    
    def summary(self) -> str:
        buses_en_ruta = 0
        buses_en_terminal = 0
        for bus in self.buses.values():
            if bus.status == bus.STATUS_EN_RUTA:
                buses_en_ruta += 1
        for bus in self.buses.values():
            if bus.status == bus.STATUS_EN_TERMINAL:
                buses_en_terminal += 1
        return f"Buses en ruta: {buses_en_ruta}, Buses en terminal: {buses_en_terminal}"