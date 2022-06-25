from OpenGL.GL import (glGenFramebuffers, glBindFramebuffer,
                       GL_FRAMEBUFFER, glDeleteFramebuffers)
from OpenGL.error import NullFunctionError


class Framebuffer:
    def create(self, buffer):
        self.FBO = glGenFramebuffers(1)
        self.bind()
        buffer.attach()
        self.unbind()

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteFramebuffers(1, self.FBO)
            self.FBO = 0
        except (NullFunctionError, TypeError):
            pass
