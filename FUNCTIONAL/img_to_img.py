from torch import autocast
from diffusers.utils import load_image
from resizer import resize_image

def img_to_img(image, pipe:str):
    with autocast("cuda"):
        load_image(image)
        image = pipe(prompt='',image=image).images[0]
    image = resize_image(image=image)
    image.save("C:/Users/aleks/Desktop/step2/output/img_to_img.png")
