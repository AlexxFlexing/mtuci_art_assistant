import sys
sys.path.append('C:/Users/aleks/Desktop/step2/FUNCTIONAL')
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk #for app itself
from PIL import ImageTk, Image #rendering image/opening image
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline #to import models and for its usage
from idea_generator import idea_generator
from txt_to_img import txt_to_img
from img_to_img import img_to_img
from img_plus_text_to_img import img_plus_text_to_img
from palette import img_to_palette


#defining several pipelines for AI
repo_id_img = "C:/Users/aleks/Desktop/step2/models/stable-diffusion-2-1"
repo_id_txt = "C:/Users/aleks/Desktop/step2/models/Llama-2-7b-Chat-AWQ"

pipe_txt_to_img = StableDiffusionPipeline.from_pretrained(repo_id_img, torch_dtype=torch.float16)
pipe_txt_to_img.to("cuda")

pipe_img_to_img = StableDiffusionImg2ImgPipeline(**pipe_txt_to_img.components)
pipe_img_to_img.to("cuda")


#creating the app
app = tk.Tk()
app.geometry("950x910")
app.title("AI artist assistant")
app.config(bg="black")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
app.iconbitmap("C:/Users/aleks/Desktop/step2/DESKTOP/interface/icon32.ico")


#placing tabs for different operations
tabview = ctk.CTkTabview(app, width=900, height=900, fg_color="#23282B")
tabview.pack(expand=True)
tabview.add("Main")
tabview.add("idea generator") #llama that takes keywords and makes a short concept that can be used as prompt for generating an image (or drawing it by yourself)
tabview.add("txt->img")  #prompt based image generation
tabview.add("img->img")  # image based image generation (remade original)
tabview.add("img->img with text") #sketch finisher using img and prompt as base
tabview.add("img->palette")  #analyzing palette of the image and outputting palette donut-type diagram and color codes
tabview.add("Credits")
tabview.set("Main")  #default tab


#forms for entering the prompts
txt_form = ctk.CTkEntry(tabview.tab("txt->img"), width=640, height=50, font=("Georgia", 25), text_color="white", fg_color="#161A1E")
txt_form.place(x=60, y=790)

txt_form_sketch = ctk.CTkEntry(tabview.tab("img->img with text"), width=570, height=50, font=("Georgia", 25), text_color="white", fg_color="#161A1E")
txt_form_sketch.place(x=60, y=790)

txt_form_idea = ctk.CTkEntry(tabview.tab("idea generator"), width=640, height=50, font=("Georgia", 25), text_color="white", fg_color="#161A1E")
txt_form_idea.place(x=60, y=790)


#label spam for main
icon = ctk.CTkImage(light_image=Image.open("C:/Users/aleks/Desktop/step2/DESKTOP/interface/icon256.ico"), dark_image=Image.open("C:/Users/aleks/Desktop/step2/DESKTOP/interface/icon256.ico"), size=(256, 256))
image=ctk.CTkLabel(tabview.tab('Main'), image=icon, text='')
image.place(x=30, y=80)

main_info = ctk.CTkLabel(tabview.tab("Main"), text="AI artist assistant", text_color="white", font=("Georgia", 50))
main_info.pack(side='top')

text = ctk.CTkLabel(tabview.tab("Main"), text="The AI artist assistant project was made for people  who are out \n of ideas for their drawings.", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=300, y=80)

text = ctk.CTkLabel(tabview.tab("Main"), text="The application has several functions those might beuseful for \n target audience.", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=300, y=130)

text = ctk.CTkLabel(tabview.tab("Main"), text="There are 5 functions: \n - idea generator", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=300, y=180)

text = ctk.CTkLabel(tabview.tab("Main"), text="the idea generator uses LLaMA 2-7B-AWQ model with \n half premade prompt, user enters their keywords for the \n concept to be generated. Concept usually describes main \n parts of the art, such as composition and so on. ", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=350, y=240)

text = ctk.CTkLabel(tabview.tab("Main"), text="- txt->img generator", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=30, y=340)

text = ctk.CTkLabel(tabview.tab("Main"), text="this generator uses Stable-diffusion v2.1 model in fp16 mode, user enters their concept or idea \n and the model generates a 768x768 image based on it. This might be useful for people who \n have certain idea that cant be easily expressed with brush or pen.", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=50, y=370)

text = ctk.CTkLabel(tabview.tab("Main"), text="- img->img generator:", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=30, y=450)

text = ctk.CTkLabel(tabview.tab("Main"), text="this generator uses Stable-diffusion v2.1 model in fp16 mode as well, user is supposed to \n select an image from his PC. It is highly recommended to use high quality images \n (768x768 or larger) for better output. This generator might be useful for people who have \n drawn an artwork or a colored sketch treimagine the art.", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=50, y=480)

text = ctk.CTkLabel(tabview.tab("Main"), text="- img->img with text generator", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=30, y=575)

text = ctk.CTkLabel(tabview.tab("Main"), text=" this generator uses Stable-diffusion v2.1 model in fp16 mode as well, user is supposed to \n select an image and fill the entry with an idea,  It is highly recommended to use high quality \n images (768x768 or larger) for better output. This generator might be useful for those who \n want to reimagine the art with certain concept to be added.", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=50, y=605)

text = ctk.CTkLabel(tabview.tab("Main"), text="- img->palette generator", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=30, y=700)

text = ctk.CTkLabel(tabview.tab("Main"), text="this function generates a donut-charted palette that shows most used colors, their hex-codes \n and the percentage of the imaged used by them, there are also presented top3 colors.\n This function might be useful for those who saw a colorful art and wanted to get the palette \n to work with.", text_color="white", font=("Georgia", 20), justify='left')    
text.place(x=50, y=730)

#text = ctk.CTkLabel(tabview.tab("Main"), text="Go ahead and try them!", text_color="white", font=("Georgia", 20), justify='left')    
#text.place(x=30, y=830)


#label spam for credits
text = ctk.CTkLabel(tabview.tab("Credits"), text="Project by \n MTUCI BVT2206 Group", text_color="white", font=("Georgia", 25))    
text.pack(anchor='center')

text = ctk.CTkLabel(tabview.tab("Credits"), text="github repo: \n https://github.com/AlexxFlexing/ai_artist_assistant.git", text_color="white", font=("Georgia", 25))    
text.pack(side='top', pady=30)

text = ctk.CTkLabel(tabview.tab("Credits"), text="Teamlead/model implementation: \n tg: @alexxflexing \n github: @alexxflexing", text_color="white", font=("Georgia", 25))    
text.pack(side='top', pady=50)

text = ctk.CTkLabel(tabview.tab("Credits"), text="Tkinter/Telegram-bot: \n tg: @NFlary \n github: @noflary", text_color="white", font=("Georgia", 25))    
text.pack(side='top', pady=50)

text = ctk.CTkLabel(tabview.tab("Credits"), text="Web-app/Palette analyzer: \n tg: @lapisuzxc \n github: @lapisuzxc", text_color="white", font=("Georgia", 25))    
text.pack(side='top', pady=50)

text = ctk.CTkLabel(tabview.tab("Credits"), text="2023", text_color="white", font=("Georgia", 25))    
text.pack(side='bottom')


#labels for outputs to be shown later
text_for_idea = ctk.CTkLabel(tabview.tab("idea generator"), text="Suggested idea:", text_color="white", font=("Georgia", 25))
text_for_idea.place(x=30, y=30)
idea_itself = ctk.CTkLabel(tabview.tab("idea generator"), text='', justify='left')
idea_itself.place(x=80, y=80)

generated_img_first = ctk.CTkLabel(tabview.tab("txt->img"), text="")
generated_img_first.pack(anchor="center")

generated_img_second = ctk.CTkLabel(tabview.tab("img->img"), text="")
generated_img_second.pack(anchor="center")

generated_img_third = ctk.CTkLabel(tabview.tab("img->img with text"), text="")
generated_img_third.pack(anchor="center")

generated_img_palette = ctk.CTkLabel(tabview.tab("img->palette"), text="")
generated_img_palette.pack(anchor="center")

colorLbl1 = ctk.CTkLabel(tabview.tab("img->palette"), text='', text_color="white", font=("Georgia", 25))
colorLbl2 = ctk.CTkLabel(tabview.tab("img->palette"), text='', text_color="white", font=("Georgia", 25))
colorLbl3 = ctk.CTkLabel(tabview.tab("img->palette"), text='', text_color="white", font=("Georgia", 25))
colorLbl1.place(x=315, y=550)
colorLbl2.place(x=315, y=600)  
colorLbl3.place(x=315, y=650)


#idea generator
def idea_gen():
    idea_itself.configure(text=idea_generator(txt_form_idea.get(), repo_id_txt), text_color="white", font=("Georgia", 25))

idea_button = ctk.CTkButton(tabview.tab("idea generator"), width=150, height=50, font=("Georgia", 25), text_color="white", fg_color="#4682B4", text="Generate", command=idea_gen)
idea_button.place(x=710, y=790)


#txt to img generator
def txt_to_img_gen():
    txt_to_img(txt_form.get(), pipe_txt_to_img)
    image = Image.open("C:/Users/aleks/Desktop/step2/output/txt_to_img.png")
    img = ImageTk.PhotoImage(image)
    generated_img_first.configure(image=img)

gen_button = ctk.CTkButton(tabview.tab("txt->img"), width=100, height=50, font=("Georgia", 25), text_color="white", fg_color="#4682B4", text="Generate", command=txt_to_img_gen)
gen_button.place(x=710, y=790)


#img to img generator
def img_to_img_gen():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image = Image.open(file_path)
        img_to_img(image, pipe_img_to_img)
        image = Image.open("C:/Users/aleks/Desktop/step2/output/img_to_img.png")
        img = ImageTk.PhotoImage(image)
        generated_img_second.configure(image=img)

img_button = ctk.CTkButton(tabview.tab("img->img"), width=260, height=50, font=("Georgia", 25), text_color="white", fg_color="#4682B4", text="Open an Image", command=img_to_img_gen)
img_button.pack(side='bottom', pady=30)


#img to img with text generator
def img_to_imgntext_gen():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image = Image.open(file_path)
        img_plus_text_to_img(image, prompt=txt_form_sketch.get(), pipe=pipe_img_to_img)
        image = Image.open("C:/Users/aleks/Desktop/step2/output/img_to_img_w_txt.png")
        img = ImageTk.PhotoImage(image)
        generated_img_third.configure(image=img)

imgngenbutton = ctk.CTkButton(tabview.tab("img->img with text"), width=150, height=50, font=("Georgia", 25), text_color="white", fg_color="#4682B4", text="Open/Generate", command=img_to_imgntext_gen)
imgngenbutton.place(x=650, y=790)


#palette generator
def img_to_palette_gen():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = Image.open(file_path)
        color_json_t = img_to_palette(img)
        #img_to_palette(file_path)
        image = Image.open("C:/Users/aleks/Desktop/step2/output/palette_donut.png")
        image = image.resize((500,500))
        img = ImageTk.PhotoImage(image)
        generated_img_palette.configure(image=img)
        colorLbl1.configure(text="Top-1 used:    "+color_json_t['color0'])
        colorLbl2.configure(text="Top-2 used:    "+color_json_t['color1'])
        colorLbl3.configure(text="Top-3 used:    "+color_json_t['color2'])

palette = ctk.CTkButton(tabview.tab("img->palette"), width=260, height=50, font=("Georgia", 25), text_color="white", fg_color="#4682B4", text="Open an Image", command=img_to_palette_gen)
palette.pack(side='bottom', pady=30)


#running the app
app.mainloop() 