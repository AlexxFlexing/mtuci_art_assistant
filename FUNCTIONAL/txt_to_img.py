from torch import autocast


def txt_to_img(prompt:str, pipe:str):
    with autocast("cuda"):
        image = pipe(prompt).images[0]
    image.save("C:/Users/aleks/Desktop/step2/output/txt_to_img.png")
