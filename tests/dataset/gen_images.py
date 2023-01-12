from PIL import Image

# генерация изображений для тестов

IMG_COLORS = ('red', 'green', 'blue')
IMG_EXT = '.png'

def gen_images():
    for color in IMG_COLORS:
        img = Image.new(mode='RGB', size=(200, 200), color=color)
        img.save(f'attachments_files/{color}{IMG_EXT}')
