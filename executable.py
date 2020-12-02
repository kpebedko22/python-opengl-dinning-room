import glfw, glm, math, json
import numpy as np
from OpenGL.GL import (glEnable, GL_DEPTH_TEST,GL_CULL_FACE,
glGetError,glClearColor,glClear,GL_COLOR_BUFFER_BIT, 
GL_DEPTH_BUFFER_BIT,glViewport,glActiveTexture,GL_TEXTURE1, 
glBindTexture,GL_TEXTURE_CUBE_MAP,GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
GL_GEOMETRY_SHADER,GL_TRUE)
from engine.base.program import Program
from engine.base.shader import Shader
from engine.base.camera import Camera
from engine.renderable.model import Model
from engine.renderable.shadow import Shadow

# получения информации о конфигурации
#
with open('config.json') as file:
    config = json.load(file)

# ширина и высота окна
#
width, height = config['window_width'], config['window_height']
light_movement = config['light_movement']

# глобальные данные для камеры и ее перемещения
#
cam = Camera()
lastX, lastY = width / 2, height / 2
first_mouse = True
left, right, forward, backward = False, False, False, False

def main():
    if not glfw.init():
        print('Failed to initialize GLFW.')
        return
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.SAMPLES, config['sampling_level'])
    
    if config['fullscreen']:
        global width, height
        mode = glfw.get_video_mode(glfw.get_primary_monitor())
        width, height = mode.size.width, mode.size.height
        window = glfw.create_window(mode.size.width, mode.size.height, config['app_name'], glfw.get_primary_monitor(), None)
    else:
        window = glfw.create_window(width, height, config['app_name'], None, None)
    if not window:
        print('Failed to create GLFW Window.')
        glfw.terminate()
        return

    # подключаем наши функции для эвентов 
    #
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, ResizeCallback)
    glfw.set_cursor_pos_callback(window, MouseLookCallback)
    glfw.set_key_callback(window, KeyInputCallback) 
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    
    # подключаем фрагментный и вершинный шейдеры
    #
    program = Program()
    program.attachShader(Shader('resources/shaders/vert.vs', GL_VERTEX_SHADER))
    program.attachShader(Shader('resources/shaders/frag.fs', GL_FRAGMENT_SHADER))
    program.link()
    
    # подключаем шейдер для создания карты теней
    #  
    depthProgram = Program()
    depthProgram.attachShader(Shader('resources/shaders/depth.vs', GL_VERTEX_SHADER))
    depthProgram.attachShader(Shader('resources/shaders/depth.fs', GL_FRAGMENT_SHADER))
    depthProgram.attachShader(Shader('resources/shaders/depth.gs', GL_GEOMETRY_SHADER))
    depthProgram.link()

    # создаем depthBuffer и frameBuffer
    #
    shadow = Shadow(config['near_plane_depth'], config['far_plane_depth'])
    shadow.create(config['shadow_width'], config['shadow_height'])

    program.use()
    program.setInt("diffuseTexture", 0)
    program.setInt("depthMap", 1)

    # позиция источника света
    #
    lightPos = glm.vec3(0.0, 2.35, 0.0)
    
    # загрузка всех объектов сцены
    #
    room = Model('resources/models/dinning_room.json')
    
    # цикл обработки
    #
    while not glfw.window_should_close(window):
        if config['debug_mode']:
            print(glGetError())

        # обработка нажатий клавиатуры для камеры
        #
        DoMovement()
        
        # движение источника света
        #
        if light_movement:
            lightPos.z = math.sin(glfw.get_time() * 0.5) * 3.0

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # обработка с помощью depthProgram - карта теней
        #
        shadow.castShadow(depthProgram, lightPos)
        room.draw(depthProgram)
        shadow.endCastShadow(program)

        
        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # обработка с помощью program - на основе полученной карты теней
        #
        program.use()
        view = cam.get_view_matrix()
        viewPos = glm.vec3(cam.camera_pos[0],cam.camera_pos[1],cam.camera_pos[2])
        perspective = glm.perspective(45, width / height, config['near_plane'], config['far_plane'])
        program.setMat4('projection', perspective)
        program.setMat4('view', view)
        program.setVec3('lightPos', lightPos)
        program.setVec3('viewPos', viewPos)
        program.setInt('shadows', True)
        program.setFloat("far_plane", config["far_plane_depth"])
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, shadow.depthbuffer.texture)
        room.draw(program)

        glfw.swap_buffers(window)
        glfw.poll_events()
        

    glfw.terminate()

def ResizeCallback(window, w, h):
    """
    Функция отслеживания изменения размеров окна приложения
    """
    global width, height
    width, height = w, h
    _perspective = glm.perspective(45, width / height, config['near_plane'], config['far_plane'])

def KeyInputCallback(window, key, scancode, action, mods):
    """
    Функция отслеживания нажатий клавиш клавиатуры
    """
    global left, right, forward, backward
    global light_movement

    # закрытие окна по нажатию на Esc
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, glfw.TRUE)

    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        light_movement = not light_movement

    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False

def DoMovement():
    """
    Функция отслеживания передвижение камеры на WASD
    """
    if left:
        cam.process_keyboard("LEFT", 0.05)
    if right:
        cam.process_keyboard("RIGHT", 0.05)
    if forward:
        cam.process_keyboard("FORWARD", 0.05)
    if backward:
        cam.process_keyboard("BACKWARD", 0.05)

def MouseLookCallback(window, xpos, ypos):
    """
    Функция отслеживания курсора мыши
    """
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

if __name__ == '__main__':
    main()