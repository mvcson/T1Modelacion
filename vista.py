import glfw
import sys
from OpenGL.GL import *
import grafica.easy_shaders as es
from controlador import Controller
from modelos import Pajaro

if __name__ == '__main__':
    if not glfw.init():
        sys.exit()

    # Hacemos la ventana
    width, height = 900, 900
    window = glfw.create_window(width, height, 'FLAPPY BIRD ÉPICO', None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)

    # Hacemos el controlador
    controller = Controller()
    glfw.set_key_callback(window, controller.on_key)

    # Pipeline
    pipeline = es.SimpleTransformShaderProgram()  # importante!
    glUseProgram(pipeline.shaderProgram)
    glClearColor(0.85, 1, 1, 1)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    # Modelos
    pajaro = Pajaro(pipeline)

    # Pasamos los modelos al controlador
    controller.pajaro = pajaro

    # While
    t0 = glfw.get_time()

    while not glfw.window_should_close(window):  # Mientras no se cierre la ventana

        ti = glfw.get_time()
        dt = ti - t0  # dt: Tiempo que paso entre dos cuadros del juego
        t0 = ti

        # Atrapamos los eventos
        glfw.poll_events()

        # Actualizamos los modelos
        glClear(GL_COLOR_BUFFER_BIT)
        pajaro.update(dt)

        # Dibujamos los modelos
        glClear(GL_COLOR_BUFFER_BIT)
        pajaro.draw(pipeline)
        glfw.swap_buffers(window)

    # Terminamos la app
    glfw.terminate()
