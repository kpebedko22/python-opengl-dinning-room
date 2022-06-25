from pyrr import vector, vector3
from math import sin, cos, radians
import glm


class Camera:
    def __init__(self):
        self.camera_pos = glm.vec3(0.0, 2.5, 0.0)
        self.camera_front = glm.vec3(0.0, 0.0, -1.0)
        self.camera_up = glm.vec3(0.0, 1.0, 0.0)
        self.camera_right = glm.vec3(1.0, 0.0, 0.0)

        self.mouse_sensitivity = 0.25
        self.jaw = -90
        self.pitch = 0

    def get_view_matrix(self):
        return glm.lookAt(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45:
                self.pitch = 45
            if self.pitch < -45:
                self.pitch = -45

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = glm.vec3(0.0, 0.0, 0.0)
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(
            vector3.cross(
                self.camera_front,
                glm.vec3(0.0, 1.0, 0.0)
            )
        )
        self.camera_up = vector.normalise(
            vector3.cross(
                self.camera_right,
                self.camera_front
            )
        )

    # Camera method for the WASD movement
    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.camera_pos += self.camera_front * velocity

        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity

        if direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity

        if direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity

    def get_front(self):
        return (self.camera_pos + self.camera_front)
