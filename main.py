from ui.main_window import MainWindow


def main():

    app = MainWindow()

    app.run()


    from services.network_service import NetworkService


    print("IP:")
    print(NetworkService.get_local_ip())

    print()

    print("Relay ID:")
    print(NetworkService.get_relay_id())


if __name__ == "__main__":

    main()