import tkinter as tk
import time
import threading

class Device:
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        self.state = False  # Default state is off

class Thermostat(Device):
    def __init__(self, device_id):
        super().__init__(device_id, 'Thermostat')
        self.temperature = 70

    def set_temperature(self, new_temperature):
        self.temperature = new_temperature

class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home System")

        self.devices = {}  # Store devices by their unique IDs
        self.device_states = {}  # Store device states
        self.status_labels = {}
        self.control_buttons = {}

        self.schedules = {}
        self.automation_rules = []

    def add_device(self, device_id, device_type):
        if device_id in self.devices:
            return  # Device with the same ID already exists
        if device_type == 'Light':
            new_device = Device(device_id, device_type)
        elif device_type == 'Thermostat':
            new_device = Thermostat(device_id)
        else:
            return  # Unsupported device type
        self.devices[device_id] = new_device
        self.device_states[device_id] = False  # Initialize state to off

        label = tk.Label(self.root, text=f"{device_type} ({device_id}): {self.device_states[device_id]}")
        label.pack()
        self.status_labels[device_id] = label

        button = tk.Button(self.root, text=f"Toggle {device_type} ({device_id})", command=lambda id=device_id: self.toggle_device(id))
        button.pack()
        self.control_buttons[device_id] = button

    def toggle_device(self, device_id):
        if device_id in self.devices:
            self.device_states[device_id] = not self.device_states[device_id]
            self.status_labels[device_id].config(text=f"{self.devices[device_id].device_type} ({device_id}): {self.device_states[device_id]}")

    def set_thermostat_temperature(self, device_id, new_temperature):
        if device_id in self.devices and isinstance(self.devices[device_id], Thermostat):
            self.devices[device_id].set_temperature(new_temperature)

    def add_schedule(self, device_id, action, time_str):
        if device_id in self.devices:
            if device_id not in self.schedules:
                self.schedules[device_id] = {}
            self.schedules[device_id][action] = time_str

    def add_automation_rule(self, trigger_device_id, trigger_condition, action_device_id, action):
        if trigger_device_id in self.devices and action_device_id in self.devices:
            rule = (trigger_device_id, trigger_condition, action_device_id, action)
            self.automation_rules.append(rule)

    def apply_automation_rules(self):
        for rule in self.automation_rules:
            trigger_device_id, trigger_condition, action_device_id, action = rule

            # Check if trigger condition is met
            if trigger_condition == "temperature":
                # Simulating thermostat triggering
                if self.devices[trigger_device_id].device_type == "Thermostat" and self.device_states[trigger_device_id]:
                    # Temperature condition met (e.g., thermostat is on)
                    self.toggle_device(action_device_id)  # Perform the action

    def start_simulation(self):
        # Start a thread for the automation rules
        automation_thread = threading.Thread(target=self.run_automation)
        automation_thread.daemon = True
        automation_thread.start()

    def run_automation(self):
        while True:
            self.apply_automation_rules()
            time.sleep(5)  # Check automation rules every 5 seconds


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)

    # Initialize devices
    app.add_device("Light1", "Light")
    app.add_device("Thermostat1", "Thermostat")
    app.add_device("Lock1", "Door Lock")

    # Define schedules
    app.add_schedule("Light1", "on", "07:00")
    app.add_schedule("Light1", "off", "23:00")

    # Define automation rules
    app.add_automation_rule("Thermostat1", "temperature", "Light1", "off")

    # Set thermostat temperature
    app.set_thermostat_temperature("Thermostat1", 75)

    # Add new light devices
    app.add_device("Light2", "Light")
    app.add_device("Light3", "Light")

    app.start_simulation()

    root.mainloop()
