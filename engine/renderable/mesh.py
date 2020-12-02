import numpy as np
from OpenGL.GL import (glGenVertexArrays, glBindVertexArray, glGenBuffers, glBindBuffer, 
glBufferData, GL_ARRAY_BUFFER, GL_STATIC_DRAW, GL_ELEMENT_ARRAY_BUFFER, glVertexAttribPointer, 
glEnableVertexAttribArray, glDrawElements, GL_TRIANGLES, GL_UNSIGNED_INT, ctypes, GL_FLOAT, GL_FALSE, glDrawArrays,
glActiveTexture, GL_TEXTURE0, glBindTexture, GL_TEXTURE_2D, glDisable,GL_CULL_FACE, glEnable)

from engine.renderable.ObjLoader import ObjLoader
from engine.renderable.texture import LoadTexture

class Mesh:
    def __init__(self, data):
        self.cull_face = data["cull_face"]

        indicesData, buffer = ObjLoader.load_model("resources/objects/obj/{}.obj".format(data["name"]))
        self.__indicesLen = len(indicesData)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

        glBindVertexArray(self.VAO)
        #  vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(0))

        #  textures
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(12))

        #  normals
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(20))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        self.texture = LoadTexture('resources/objects/texture/{}'.format(data["texture_name"]))

    def draw(self, program):
        if self.cull_face:
            glDisable(GL_CULL_FACE)
        
        program.setInt("diffuseTexture", 0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self.__indicesLen)
        glBindVertexArray(0)

        if self.cull_face:
            glEnable(GL_CULL_FACE)

