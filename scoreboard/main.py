from Simulator.ControlUnit import ControlUnit



if __name__ == '__main__':
    central_control = ControlUnit("test2.in")

    while not central_control.done():
        central_control.tick()
