import threading
import time
import pystray
from PIL import Image
import keyboard
import sys

# Global state
active = True  # Start as active
stop_event = threading.Event()  # Event to control the keep_awake thread

# Constants
STATES = {
    True: {'label': 'Active', 'color': 'green'},
    False: {'label': 'Inactive', 'color': 'red'}
}

# Cached images
images = {state: Image.new('RGB', (16, 16), data['color']) for state, data in STATES.items()}

# Function to simulate keypress
def keep_awake():
    while not stop_event.is_set():  # Run until the stop_event is set
        if active:
            keyboard.press_and_release('f15')  # Simulate F15 keypress
        time.sleep(59)  # Wait for 59 seconds

# Function to toggle the state
def toggle_state(icon, item=None):
    global active
    active = not active
    icon.icon = images[active]
    update_menu(icon)

    # Restart the keep_awake thread if active
    if active:
        stop_event.clear()  # Clear the stop event
        thread = threading.Thread(target=keep_awake, daemon=True)
        thread.start()
    else:
        stop_event.set()  # Set the stop event to stop the thread

# Function to update the menu with the correct label
def update_menu(icon):
    icon.menu = pystray.Menu(
        pystray.MenuItem(
            STATES[active]['label'],
            toggle_state,
            checked=lambda item: active,
            radio=True,
            default=True
        ),
        pystray.MenuItem(
            'Exit',
            exit_app
        )
    )
    icon.update_menu()

# Function to exit the application
def exit_app(icon, item):
    global active
    active = False  # Stop the keep_awake loop
    stop_event.set()  # Ensure the thread stops
    icon.stop()
    sys.exit()

# Create the system tray icon
icon = pystray.Icon(
    'caffeine',
    icon=images[active],
    menu=pystray.Menu(
        pystray.MenuItem(
            STATES[active]['label'],
            toggle_state,
            checked=lambda item: active,
            radio=True,
            default=True
        ),
        pystray.MenuItem(
            'Exit',
            exit_app
        )
    )
)

# Start the keypress simulation in a separate thread
thread = threading.Thread(target=keep_awake, daemon=True)
thread.start()

# Run the system tray icon
icon.run()