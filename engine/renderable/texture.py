import glm
from OpenGL.GL import (glGenTextures, glBindTexture, GL_TEXTURE_2D, 
glTexParameteri,GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, 
GL_LINEAR,GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE, GL_TEXTURE_WRAP_T, 
GL_REPEAT, glTexImage2D, GL_TEXTURE_COMPARE_MODE, GL_COMPARE_REF_TO_TEXTURE, 
GL_DEPTH_COMPONENT, GL_FLOAT, glActiveTexture , GL_TEXTURE0, GL_RGBA, GL_UNSIGNED_BYTE, GL_LINEAR_MIPMAP_LINEAR, glGenerateMipmap)

from PIL import Image

def LoadTexture(path):

    # запросим у OpenGL свободный индекс текстуры
    texture = glGenTextures(1)

    # сделаем текстуру активной
    glBindTexture(GL_TEXTURE_2D, texture)

    # загружаем изображение-текстуру
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    # установим параметры фильтрации текстуры - линейная фильтрация
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # установим параметры "оборачиваниея" текстуры - отсутствие оборачивания
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) #GL_REPEAT
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) #GL_REPEAT
    
    # возвращаем текстуру
    return texture