from app.model import Bus, TransportManager


class TransportManagerInterface:
    def __init__(self, transport_manager: TransportManager):
        self.transport_manager = transport_manager
        self.load_initial_data()

    def load_initial_data(self):
        buses = [
            {"capacity": 50},
            {"capacity": 30},
            {"capacity": 40}
        ]
        for bus in buses:
            self.transport_manager.add_bus(bus["capacity"])

    def run(self):
        while True:
            print("\nSistema de Simulación de Transporte Urbano")
            print("1. Agregar autobús")
            print("2. Asignar ruta a autobús")
            print("3. Ver autobuses por estado")
            print("4. Ver autobuses por ruta")
            print("5. Actualizar estado de autobús")
            print("6. Actualizar asientos ocupados")
            print("7. Actualizar ubicación de autobús")
            print("8. Calcular distancia a un destino")
            print("9. Ver resumen de autobuses")
            print("10. Salir")

            option = input("\nSelecciona una opción: ")

            if option == '1':
                self.add_bus()
            elif option == '2':
                self.assign_route()
            elif option == '3':
                self.show_buses_by_status()
            elif option == '4':
                self.show_buses_by_route()
            elif option == '5':
                self.update_bus_status()
            elif option == '6':
                self.update_occupied_seats()
            elif option == '7':
                self.update_bus_location()
            elif option == '8':
                self.calculate_distance_to_destination()
            elif option == '9':
                self.show_summary()
            elif option == '10':
                print("Adios!")
                break

    def add_bus(self):
        capacity = int(input("Capacidad del autobús: "))
        bus_id = self.transport_manager.add_bus(capacity)
        print(f"Autobús agregado con ID: {bus_id} y capacidad: {capacity}")

    def assign_route(self):
        bus_id = int(input("Introduce el ID del autobús: "))
        route = input("Ruta del autobús: ")
        if bus_id in self.transport_manager.buses:
            self.transport_manager.assign_route(bus_id, route)
            print(f"Ruta '{route}' asignada al autobús con ID {bus_id}")

    def show_buses_by_status(self):
        status = input(f"Introduce el estado ({Bus.STATUS_EN_RUTA}, {Bus.STATUS_EN_TERMINAL}): ")
        buses = self.transport_manager.buses_by_status(status)
        self.show_buses(buses)

    def show_buses_by_route(self):
        route = input("Introduce la ruta: ")
        buses = self.transport_manager.buses_by_route(route)
        self.show_buses(buses)

    def update_bus_status(self):
        bus_id = int(input("Introduce el ID del autobús: "))
        if bus_id in self.transport_manager.buses:
            self.transport_manager.buses[bus_id].toggle_status()
            print(f"Estado del autobús con ID {bus_id} actualizado")

    def update_occupied_seats(self):
        bus_id = int(input("Introduce el ID del autobús: "))
        if bus_id in self.transport_manager.buses:
            occupied_seats = int(input("Introduce el número de asientos ocupados: "))
            self.transport_manager.buses[bus_id].update_occupied_seats(occupied_seats)
            print(f"Asientos ocupados del autobús con ID {bus_id} actualizados a {occupied_seats}")

    def update_bus_location(self):
        bus_id = int(input("Introduce el ID del autobús: "))
        if bus_id in self.transport_manager.buses:
            new_x = int(input("Introduce la nueva coordenada X: "))
            new_y = int(input("Introduce la nueva coordenada Y: "))
            self.transport_manager.update_bus_location(bus_id, new_x, new_y)
            print(f"Ubicación del autobús con ID {bus_id} actualizada a ({new_x}, {new_y})")

    def calculate_distance_to_destination(self):
        bus_id = int(input("Introduce el ID del autobús: "))
        if bus_id in self.transport_manager.buses:
            destination_x = int(input("Introduce la coordenada X del destino: "))
            destination_y = int(input("Introduce la coordenada Y del destino: "))
            distance = self.transport_manager.calculate_distance_to_destination(bus_id, destination_x, destination_y)
            if distance != -1:
                print(f"La distancia desde la ubicación actual del autobús con ID {bus_id} al destino es: {distance:.2f} unidades")

    def show_summary(self):
        summary = self.transport_manager.summary()
        print(summary)

    def show_buses(self, buses):
        if not buses:
            print("No se encontraron autobuses")
            return

        print("\nLista de Autobuses:")
        for bus in buses:
            print(f"ID: {bus.id}, Ruta: {bus.route}, Capacidad: {bus.capacity}, Asientos Ocupados: {bus.occupied_seats}, Estado: {bus.status}, Ubicación: {bus.location}")
