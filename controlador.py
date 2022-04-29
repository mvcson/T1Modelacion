import glfw
import sys
from modelos import Pajaro
from typing import Optional


class Controller(object):
    pajaro: Optional['Pajaro']
    tubo: Optional['Tubo']

    def __init__(self):  # Referencias a objetos
        self.pajaro = None
        self.tubo = None

    def set_model(self, m):
        self.pajaro = m

    def set_tubo(self, e):
        self.tubo = e

    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):  # Particular de la app
            return
        if key == glfw.KEY_ESCAPE:
            glfw.terminate()
            sys.exit()

        # Le pasa los eventos a los modelos
        elif key == glfw.KEY_UP and action == glfw.PRESS:
            self.pajaro.move_up()

