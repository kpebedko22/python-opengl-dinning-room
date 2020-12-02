import os, json, glm
import numpy as np
from engine.renderable.mesh import Mesh 

class Model:
    def __init__(self, path):
        self.meshes = []
        if not os.path.exists(path):
            raise RuntimeError(f'Model source file {path} does not exists.')
        self.path = path
        self.model = glm.mat4(1.0)
        data = self.__loadAndGetData()
        
        for name in data["names"]:
            self.meshes.append(Mesh(data[name]))

    def __loadAndGetData(self):
        data = None
        with open(self.path) as file:
            data = json.load(file)
        return data

    def draw(self, program):
        program.use()
        program.setMat4('model', self.model)

        for mesh in self.meshes:
            mesh.draw(program)

    def __del__(self):
        self.delete()

    def delete(self):
        self.meshes.clear()