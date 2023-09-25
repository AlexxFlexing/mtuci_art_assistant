from torch import autocast
from diffusers.utils import load_image
from resizer import resize_image

def img_plus_text_to_img(image, prompt:str, pipe:str):
    with autocast("cuda"):
        load_image(image)
        image = pipe(image=image, prompt=prompt).images[0]
    image = resize_image(image=image)
    image.save("C:/Users/aleks/Desktop/step2/output/img_to_img_w_txt.png")
