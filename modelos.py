import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
from OpenGL.GL import GL_STATIC_DRAW
import random
from typing import List
from numpy import *

def create_gpu(shape, pipeline):
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpu


class Pajaro(object):

    def __init__(self, pipeline):
        # Modelación jerárquica con grafo
        gpu_body_quad = create_gpu(bs.createColorQuad(0.8, 0.7, 0.4), pipeline)  # cafe claro
        gpu_pico_quad = create_gpu(bs.createColorQuad(0.2, 0.1, 0), pipeline)  # cafe
        gpu_eye_quad = create_gpu(bs.createColorQuad(1, 1, 1), pipeline)  # blanco
        gpu_ala_quad = create_gpu(bs.createColorQuad(0.6, 0.5, 0.3), pipeline) #blanco

        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(1)
        body.childs += [gpu_body_quad]

        # Creamos el pico
        pico = sg.SceneGraphNode('Pico') 
        pico.transform = tr.scale(0.6, 0.3, 1)
        pico.childs += [gpu_pico_quad]

        # Rotacion del pico del pájaro
        rot_pico = sg.SceneGraphNode('rotar pico')
        rot_pico.transform = tr.translate(0.55, -0.05, 0)  # tr.matmul([])..
        rot_pico.childs += [pico]

        # Ojitos
        eye = sg.SceneGraphNode('eye')
        eye.transform = tr.scale(0.2, 0.2, 1)
        eye.childs += [gpu_eye_quad]

        eye_der = sg.SceneGraphNode('eyeRight')
        eye_der.transform = tr.translate(0.28, 0.3, 0)
        eye_der.childs += [eye]

        # Ala
        ala = sg.SceneGraphNode('ala')
        ala.transform = tr.scale(0.36, 0.7, 1)
        ala.childs += [gpu_ala_quad]

        # Rot Ala
        rot_ala = sg.SceneGraphNode('rotar ala')
        rot_ala.transform = tr.translate(-0.15, -0.3, 0)
        rot_ala.childs += [ala]

        # Ensamblamos el mono
        mono = sg.SceneGraphNode('pajaro')
        mono.transform = tr.matmul([tr.scale(0.15, 0.15, 0), tr.translate(0, 0, 0)])
        mono.childs += [body, rot_pico, rot_ala, eye_der]

        transform_mono = sg.SceneGraphNode('pajaroTR')
        transform_mono.childs += [mono]

        self.model = transform_mono
        self.pos_y = 0.4 
        self.pos_x = 0
        self.alive = True

    def move_up(self):
        self.pos_y += 0.2

    def draw(self, pipeline):
            self.model.transform = tr.translate(0.7 * self.pos_x, self.pos_y, 0)
            sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def update(self, dt):
        self.pos_y -= dt

class Tubo(object):

    def __init__(self, pipeline):
        gpu_tubo = create_gpu(bs.createColorQuad(0.7, .7, .7), pipeline)

        tubo = sg.SceneGraphNode('tubo')
        tubo.transform = tr.scale(0.1, 0.2, 1)
        tubo.childs += [gpu_tubo]

        tubo_tr = sg.SceneGraphNode('tuboTR')
        tubo_tr.childs += [tubo]

        self.pos_y = random.choice([-1, 0, 1])
        self.pos_x = 1
        self.model = tubo_tr

    def draw(self, pipeline):
        self.model.transform = tr.translate(self.pos_x, 0.7 * self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def update(self, dt):
        dt *= 10
        if self.pos == 1:
            self.x += dt  # no lineal, cos(...)
            if self.x > 0:
                self.x = min(0.7, self.x)
        elif self.pos == 0:
            if abs(self.x) < 0.05:
                self.x = 0
            else:
                if self.x < 0:
                    self.x += dt
                elif self.x > 0:
                    self.x -= dt
        elif self.pos == -1:
            self.x -= dt
            self.x = max(-0.7, self.x)
        # modificar de manera constante al modelo
        # aqui deberia llamar a tr.translate
        self.modifymodel()

