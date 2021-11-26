# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 18:59:28 2021

@author: hugo_
"""

import pygame
import glm
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from obj import Obj


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.modelList = []
        self.activeModelIndex = 0
        self.shaderList = []
        self.activeShaderIndex = 0

        self.camPosition = glm.vec3(0, 0, 0)
        self.camRotation = glm.vec3(0, 0, 0)

        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

        self.pointLight = glm.vec4(0,0,0,0)

        self.angle = 0
        self.viewMatrix = self.getViewMatrix()

        self.rotYaw = 0
        self.rotPitch = 0
        self.rotRoll = 0
    
    def getViewMatrix(self):
        i = glm.mat4(1)
        camTranslate = glm.translate(i, self.camPosition)
        camPitch = glm.rotate(i, glm.radians(self.camRotation.x), glm.vec3(1,0,0))
        camYaw   = glm.rotate(i, glm.radians(self.camRotation.y), glm.vec3(0,1,0))
        camRoll  = glm.rotate(i, glm.radians(self.camRotation.z), glm.vec3(0,0,1))
        camRotate = camPitch * camYaw * camRoll

        return glm.inverse(camTranslate * camRotate)

    def cameraView(self):
        r = (self.camPosition.x ** 2 + self.camPosition.z ** 2) ** 0.5
        self.camPosition.x = r * math.cos(self.angle * math.pi / 180)
        self.camPosition.z = r * math.sin(self.angle * math.pi / 180)
        self.viewMatrix = glm.lookAt(self.camPosition, self.modelList[self.activeModelIndex].position, glm.vec3(0, 1, 0))


    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def translateCube(self, x, y, z):
        self.cubePos = glm.vec3(x,y,z)

    # Rotacion en eje X
    def rotaPitch(self):
        self.rotPitch += 5

    # Rotacion en eje Y
    def rotaYaw(self):
        self.rotYaw += 5

    # Rotacion en eje Z
    def rotaRoll(self):
        self.rotRoll += 5

    def setShaders(self, vertexShader, fragShader):
        if vertexShader is not None or fragShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER), compileShader(fragShader, GL_FRAGMENT_SHADER), validate=False)
        else:
            self.active_shader = None

        glUseProgram(self.active_shader)

    def createObjects(self):
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, rectVerts.nbytes, rectVerts, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, rectIndices.nbytes, rectIndices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)

    def render(self):
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"), 1, GL_FALSE, glm.value_ptr(self.viewMatrix))
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projection"), 1, GL_FALSE, glm.value_ptr(self.projection))
            glUniform4f(glGetUniformLocation(self.active_shader, "light"), self.pointLight.x, self.pointLight.y, self.pointLight.z, self.pointLight.w)
            glUniform4f(glGetUniformLocation(self.active_shader, "color"), 1, 1, 1, 1)


        
        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"), 1, GL_FALSE, glm.value_ptr(self.modelList[self.activeModelIndex].getMatrix()))

            self.modelList[self.activeModelIndex].renderInScene()


    
    
    
