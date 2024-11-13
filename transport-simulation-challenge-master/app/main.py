from app.model import TransportManager
from app.ui_console import TransportManagerInterface


def main():
    transport_manager = TransportManager()
    interface = TransportManagerInterface(transport_manager)
    interface.run()


if __name__ == "__main__":
    main()
