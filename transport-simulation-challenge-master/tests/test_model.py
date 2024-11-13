import unittest
from dataclasses import is_dataclass
from inspect import signature, getmembers, isclass
import app.model as model_module


# Check if classes are defined in the module
def has_class(module, class_name):
    return class_name in [name for name, _ in getmembers(module, isclass)]


class TestBus(unittest.TestCase):
    def setUp(self):
        if has_class(model_module, 'Bus'):
            self.bus = model_module.Bus(id=1, capacity=50)

        if self._testMethodDoc:
            self._testMethodDoc = self._testMethodDoc.strip()

    @unittest.skipUnless(has_class(model_module, 'Bus'), "La clase Bus no está definida.")
    def test_is_dataclass(self):
        """Verifica si Bus es una dataclass."""
        self.assertTrue(is_dataclass(self.bus))

    def test_class_variables_exist_and_correct_type(self):
        """Verifica que las constantes de la clase Bus existan y tengan el tipo correcto."""
        class_variables = [
            ('STATUS_EN_RUTA', str),
            ('STATUS_EN_TERMINAL', str)
        ]
        for var_name, var_type in class_variables:
            with self.subTest(var_name=var_name):
                if not has_class(model_module, 'Bus'):
                    self.fail("La clase Bus no está definida.")
                self.assertTrue(hasattr(model_module.Bus, var_name))
                self.assertIsInstance(getattr(model_module.Bus, var_name), var_type)

    def test_instance_attributes_exist(self):
        """Verifica que los atributos de instancia de la clase Bus existan."""
        instance_attributes = ['id', 'route', 'capacity', 'occupied_seats', 'status', 'location']
        for attr_name in instance_attributes:
            with self.subTest(attr_name=attr_name):
                if not has_class(model_module, 'Bus'):
                    self.fail("La clase Bus no está definida.")
                self.assertTrue(hasattr(self.bus, attr_name))

    def test_methods_are_defined(self):
        """Verifica que los métodos de la clase Bus estén definidos con las firmas correctas."""
        methods = [
            ('assign_route', '(route: str)'),
            ('update_occupied_seats', '(occupied_seats: int)'),
            ('toggle_status', '()'),
            ('update_location', '(new_x: int, new_y: int)'),
            ('calculate_distance', '(dest_x: int, dest_y: int) -> float')
        ]
        for method_name, expected_signature in methods:
            with self.subTest(method_name=method_name):
                if not has_class(model_module, 'Bus'):
                    self.fail("La clase Bus no está definida.")
                method = getattr(self.bus, method_name, None)
                self.assertTrue(callable(method))
                self.assertEqual(str(signature(method)), expected_signature)

    def test_assign_route_valid_routes(self):
        """Verifica la asignación de rutas válidas en la clase Bus."""
        routes = ["Ruta A", "Ruta B", "Ruta C"]
        for route in routes:
            with self.subTest(route=route):
                if not has_class(model_module, 'Bus'):
                    self.fail("La clase Bus no está definida.")
                self.bus.assign_route(route)
                self.assertEqual(self.bus.route, route)

    def test_update_occupied_seats(self):
        """Verifica la actualización de asientos ocupados con valores válidos y no válidos en la clase Bus."""
        test_cases = [
            (25, 25),
            (60, 0),  # No debe exceder la capacidad, debe permanecer en 0
            (-5, 0)   # No debe ser negativo, debe permanecer en 0
        ]
        for occupied_seats, expected_result in test_cases:
            with self.subTest(occupied_seats=occupied_seats):
                if not has_class(model_module, 'Bus'):
                    self.fail("La clase Bus no está definida.")
                self.bus.occupied_seats = 0  # Reiniciar el valor antes de cada subtest
                self.bus.update_occupied_seats(occupied_seats)
                self.assertEqual(self.bus.occupied_seats, expected_result)

    def test_toggle_status(self):
        """Verifica el cambio de estado del bus entre 'en ruta' y 'en la terminal' en la clase Bus."""
        initial_status = self.bus.status
        self.bus.toggle_status()
        self.assertNotEqual(self.bus.status, initial_status)
        self.assertEqual(self.bus.status, model_module.Bus.STATUS_EN_RUTA)
        self.bus.toggle_status()
        self.assertEqual(self.bus.status, model_module.Bus.STATUS_EN_TERMINAL)

    def test_update_location_valid_coordinates(self):
        """Verifica la actualización de la ubicación con coordenadas válidas en la clase Bus."""
        locations = [(10, 20), (15, 30), (0, 0)]
        for new_x, new_y in locations:
            with self.subTest(new_x=new_x, new_y=new_y):
                if not has_class(model_module, 'Bus'):
                    self.fail("La clase Bus no está definida.")
                self.bus.update_location(new_x, new_y)
                self.assertEqual(self.bus.location, (new_x, new_y))

    def test_calculate_distance_valid_scenarios(self):
        """Verifica el cálculo de distancia con escenarios válidos en la clase Bus."""
        test_cases = [
            ((0, 0), (3, 4), 5.0),  # Triángulo 3-4-5
            ((1, 1), (4, 5), 5.0),
            ((0, 0), (6, 8), 10.0)  # Triángulo 6-8-10
        ]
        for start_location, destination, expected_distance in test_cases:
            with self.subTest(start_location=start_location, destination=destination):
                if not has_class(model_module, 'Bus'):
                    self.fail("La clase Bus no está definida.")
                self.bus.update_location(*start_location)
                distance = self.bus.calculate_distance(*destination)
                self.assertEqual(distance, expected_distance)


class TestTransportManager(unittest.TestCase):
    def setUp(self):
        if has_class(model_module, 'TransportManager'):
            self.manager = model_module.TransportManager()
            self.bus_id = self.manager.add_bus(capacity=50)

        if self._testMethodDoc:
            self._testMethodDoc = self._testMethodDoc.strip()

    def test_methods_are_defined(self):
        """Verifica que los métodos de TransportManager estén definidos con las firmas correctas."""
        methods = [
            ('add_bus', '(capacity: int) -> int'),
            ('assign_route', '(bus_id: int, route: str)'),
            ('buses_by_status', '(status: str) -> list[app.model.Bus]'),
            ('buses_by_route', '(route: str) -> list[app.model.Bus]'),
            ('update_bus_location', '(bus_id: int, new_x: int, new_y: int)'),
            ('calculate_distance_to_destination', '(bus_id: int, destination_x: int, destination_y: int) -> float'),
            ('summary', '() -> str')
        ]
        for method_name, expected_signature in methods:
            with self.subTest(method_name=method_name):
                if not has_class(model_module, 'TransportManager'):
                    self.fail("La clase TransportManager no está definida.")
                method = getattr(self.manager, method_name, None)
                self.assertTrue(callable(method))
                self.assertEqual(str(signature(method)), expected_signature)

    @unittest.skipUnless(has_class(model_module, 'TransportManager'), "La clase TransportManager no está definida.")
    def test_add_bus_valid_capacity(self):
        """Verifica la adición de un bus con una capacidad válida en la clase TransportManager."""
        self.assertEqual(len(self.manager.buses), 1)
        self.assertEqual(self.manager.buses[self.bus_id].capacity, 50)

    def test_assign_route_valid_routes(self):
        """Verifica la asignación de rutas válidas a un bus en la clase TransportManager."""
        routes = ["Ruta B", "Ruta D", "Ruta E"]
        for route in routes:
            with self.subTest(route=route):
                if not has_class(model_module, 'TransportManager'):
                    self.fail("La clase TransportManager no está definida.")
                self.manager.assign_route(self.bus_id, route)
                self.assertEqual(self.manager.buses[self.bus_id].route, route)

    @unittest.skipUnless(has_class(model_module, 'TransportManager'), "La clase TransportManager no está definida.")
    def test_buses_by_status(self):
        """Verifica la obtención de buses por estado (en la terminal y en ruta) en la clase TransportManager."""
        buses_at_terminal = self.manager.buses_by_status(model_module.Bus.STATUS_EN_TERMINAL)
        self.assertEqual(len(buses_at_terminal), 1)
        self.manager.buses[self.bus_id].toggle_status()
        buses_on_route = self.manager.buses_by_status(model_module.Bus.STATUS_EN_RUTA)
        self.assertEqual(len(buses_on_route), 1)

    def test_buses_by_route_valid_routes(self):
        """Verifica la obtención de buses por ruta asignada en la clase TransportManager."""
        routes = ["Ruta C", "Ruta F"]
        for route in routes:
            with self.subTest(route=route):
                if not has_class(model_module, 'TransportManager'):
                    self.fail("La clase TransportManager no está definida.")
                self.manager.assign_route(self.bus_id, route)
                buses_on_route = self.manager.buses_by_route(route)
                self.assertEqual(len(buses_on_route), 1)
                self.assertEqual(buses_on_route[0].route, route)

    def test_update_bus_location_valid_coordinates(self):
        """Verifica la actualización de la ubicación de un bus con coordenadas válidas en la clase TransportManager."""
        locations = [(15, 25), (0, 0), (10, 10)]
        for new_x, new_y in locations:
            with self.subTest(new_x=new_x, new_y=new_y):
                if not has_class(model_module, 'TransportManager'):
                    self.fail("La clase TransportManager no está definida.")
                self.manager.update_bus_location(self.bus_id, new_x, new_y)
                self.assertEqual(self.manager.buses[self.bus_id].location, (new_x, new_y))

    def test_calculate_distance_to_destination_valid_scenarios(self):
        """Verifica el cálculo de la distancia de un bus hacia un destino en la clase TransportManager"""
        test_cases = [
            ((0, 0), (6, 8), 10.0),
            ((1, 1), (4, 5), 5.0),
            ((2, 3), (5, 7), 5.0)
        ]
        for start_location, destination, expected_distance in test_cases:
            with self.subTest(start_location=start_location, destination=destination):
                if not has_class(model_module, 'TransportManager'):
                    self.fail("La clase TransportManager no está definida.")
                self.manager.update_bus_location(self.bus_id, *start_location)
                distance = self.manager.calculate_distance_to_destination(self.bus_id, *destination)
                self.assertEqual(distance, expected_distance)

    @unittest.skipUnless(has_class(model_module, 'TransportManager'), "La clase TransportManager no está definida.")
    def test_summary(self):
        """Verifica el resumen del estado de los buses (en ruta y en la terminal) en la clase TransportManager."""
        summary = self.manager.summary()
        self.assertEqual(summary, "Buses en ruta: 0, Buses en terminal: 1")
        self.manager.buses[self.bus_id].toggle_status()
        summary = self.manager.summary()
        self.assertEqual(summary, "Buses en ruta: 1, Buses en terminal: 0")


if __name__ == "__main__":
    unittest.main()
