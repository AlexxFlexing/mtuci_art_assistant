from PIL import Image


def resize_image(image):
    width, height = image.size
    if width > height:
        output_width = 768
        w_percent = (output_width)/float(image.size[0])
        h_size = int((float(image.size[1])*float(w_percent)))
        image = image.resize((output_width,h_size), Image.LANCZOS)
    else:
        output_height = 768
        h_percent = (output_height)/float(image.size[1])
        w_size = int((float(image.size[0])*float(h_percent)))
        image = image.resize((w_size,output_height), Image.LANCZOS)
    return image