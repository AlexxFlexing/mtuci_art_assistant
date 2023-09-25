import sys
sys.path.append('C:/Users/aleks/Desktop/step2/FUNCTIONAL')
from PIL import ImageTk, Image #rendering image/opening image
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline #to import models and for its usage
from idea_generator import idea_generator
from txt_to_img import txt_to_img
from img_to_img import img_to_img
from img_plus_text_to_img import img_plus_text_to_img
from palette import img_to_palette
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram_token import token

#creating a bot
bot = Bot(token=token)
dp = Dispatcher(bot)


#defining several pipelines for AI
repo_id_img = "C:/Users/aleks/Desktop/step2/models/stable-diffusion-2-1"
repo_id_txt = "C:/Users/aleks/Desktop/step2/models/Llama-2-7b-Chat-AWQ"

pipe_txt_to_img = StableDiffusionPipeline.from_pretrained(repo_id_img, torch_dtype=torch.float16)
pipe_txt_to_img.to("cuda")

pipe_img_to_img = StableDiffusionImg2ImgPipeline(**pipe_txt_to_img.components)
pipe_img_to_img.to("cuda")


#handling the first bot's message
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    button_start = InlineKeyboardButton('Continue', callback_data='button_start')
    markup = InlineKeyboardMarkup().add(button_start)
    await message.answer(text="Welcome to the AI Artist Assistant project. Click the button to continue.", reply_markup=markup)


#main
@dp.callback_query_handler(lambda c: c.data == 'button_start' or c.data == 'button_back')
async def process_callback_button(callback_query: types.CallbackQuery):
    with open('C:/Users/aleks/Desktop/step2/TELEGRAM/icon256.png', 'rb') as file:
        images_bytes = file.read()
    buttons_first_row = [
        InlineKeyboardButton('Idea Generator', callback_data='button_idea_gen'),
        InlineKeyboardButton('txt->img', callback_data='button_txt_to_img'),
        InlineKeyboardButton('img->img', callback_data='button_img_to_img')
    ]
    buttons_second_row = [
        InlineKeyboardButton('img+text->img', callback_data='button_img_n_text_to_img'),
        InlineKeyboardButton('img->palette', callback_data='button_palette'),
        InlineKeyboardButton('Credits', callback_data='button_credits')
    ]
    markup_main = InlineKeyboardMarkup(row_width=3)
    markup_main.add(*buttons_first_row)
    markup_main.add(*buttons_second_row)
    await bot.send_photo(chat_id=callback_query.from_user.id, photo=images_bytes, caption='The AI artist assistant project was made for people who are out of ideas for their drawings. The application has several functions those might be useful for target audience.', reply_markup=markup_main)

#idea generator
@dp.callback_query_handler(lambda c: c.data == 'button_idea_gen')
async def process_callback_button2(callback_query: types.CallbackQuery):
    button_back = InlineKeyboardButton('Back', callback_data='button_back')
    markup_idea_gen = InlineKeyboardMarkup().add(button_back)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Start your prompt with "-g" as a flag.\nThe idea generator uses LLaMA 2-7B-AWQ model with half-premade prompt, user enters their keywords for the concept to be generated. Concept usually describes main parts of the art, such as composition and so on.', reply_markup=markup_idea_gen)


#txt->img
@dp.callback_query_handler(lambda c: c.data == 'button_txt_to_img')
async def process_callback_button2(callback_query: types.CallbackQuery):
    button_back = InlineKeyboardButton('Back', callback_data='button_back')
    markup_idea_gen_c = InlineKeyboardMarkup().add(button_back)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Start your prompt with "-t" as a flag.\nThis generator uses Stable-diffusion v2.1 model in fp16 mode, user enters their concept or idea and the model generates a 768x768 image based on it. This might be useful for people who have certain idea that cant be easily expressed with brush or pen.', reply_markup=markup_idea_gen_c)

#handling every text typed message
@dp.message_handler(content_types=types.ContentType.TEXT)
async def text_handler(message: types.Message):
    button_back = InlineKeyboardButton('Back', callback_data='button_back')
    markup_idea_gen_b = InlineKeyboardMarkup().add(button_back)
    if message.text.startswith("-g "):
        temp_text = message.text.replace("-g ","")
        await bot.send_message(chat_id=message.chat.id, text=idea_generator(temp_text, repo_id_txt), reply_markup=markup_idea_gen_b)
    elif message.text.startswith("-t "):
        temp_text_a = message.text.replace("-t ","")
        txt_to_img(temp_text_a, pipe_txt_to_img)
        with open("C:/Users/aleks/Desktop/step2/output/txt_to_img.png", 'rb') as file:
            images_bytes_first = file.read()
        await bot.send_photo(chat_id=message.chat.id, photo=images_bytes_first, caption=f'Image generated using {temp_text_a} as a prompt', reply_markup=markup_idea_gen_b)


#img->img
@dp.callback_query_handler(lambda c: c.data == 'button_img_to_img')
async def process_callback_button2(callback_query: types.CallbackQuery):
    button_back = InlineKeyboardButton('Back', callback_data='button_back')
    markup_idea_gen_f = InlineKeyboardMarkup().add(button_back)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Send a photo and put a "-p" flag as a caption.\nThis generator uses Stable-diffusion v2.1 model in fp16 mode as well, user is supposed to select an image from his PC. It is highly recommended to use high quality images (768x768 or larger) for better output. This generator might be useful for people who have drawn an artwork or a colored sketch to reimagine the art.', reply_markup=markup_idea_gen_f)


#img+text->img
@dp.callback_query_handler(lambda c: c.data == 'button_img_n_text_to_img')
async def process_callback_button2(callback_query: types.CallbackQuery):
    button_back = InlineKeyboardButton('Back', callback_data='button_back')
    markup_idea_gen_g = InlineKeyboardMarkup().add(button_back)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Send a photo, start the prompt with "-i" flag.\nThis generator uses Stable-diffusion v2.1 model in fp16 mode as well, user is supposed to select an image and fill the entry with an idea,  It is highly recommended to use high quality images (768x768 or larger) for better output. This generator might be useful for those who want to reimagine the art with certain concept to be added.', reply_markup=markup_idea_gen_g)


#palette
@dp.callback_query_handler(lambda c: c.data == 'button_palette')
async def process_callback_button2(callback_query: types.CallbackQuery):
    button_back = InlineKeyboardButton('Back', callback_data='button_back')
    markup_idea_gen_d = InlineKeyboardMarkup().add(button_back)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Send a photo and put a "-c" flag as a caption.\nThis function generates a donut-charted palette that shows most used colors, their hex-codes and the percentage of the imaged used by them, there are also presented top3 colors. This function might be useful for those who saw a colorful art and wanted to get the palette to work with.', reply_markup=markup_idea_gen_d)


#credits
@dp.callback_query_handler(lambda c: c.data == 'button_credits')
async def process_callback_button2(callback_query: types.CallbackQuery):
    button_back = InlineKeyboardButton('Back', callback_data='button_back')
    markup_idea_gen_h = InlineKeyboardMarkup().add(button_back)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Project by:\nMTUCI BVT2206 Group\n\ngithub repo: https://github.com/AlexxFlexing/ai_artist_assistant.git\n\nTeamlead/model implementation: \ntg: @alexxflexing, github: @alexxflexing\n\nTkinter:\ntg: @NFlary, github: @noflary\n\nTelegram-bot/Palette analyzer:\ntg: @lapisuzxc, github: @lapisuzxc\n2023', reply_markup=markup_idea_gen_h)


#handling every image
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo_handler(message: types.Message):
    button_back = InlineKeyboardButton('Back', callback_data='button_back')
    markup_idea_gen_e = InlineKeyboardMarkup().add(button_back)
    if "-p" in message.caption:
        photo_file_id = message.photo[-1].file_id
        photo = await bot.get_file(photo_file_id)
        photo_path = photo.file_path
        await photo.download(photo_path)
        pil_image = Image.open(photo_path)
        img_to_img(pil_image, pipe_img_to_img)
        with open("C:/Users/aleks/Desktop/step2/output/img_to_img.png", 'rb') as file:
            images_bytes_second = file.read()
        await bot.send_photo(chat_id=message.chat.id, photo=images_bytes_second, caption=f'Image generated using sent image as base', reply_markup=markup_idea_gen_e)
    elif message.caption.startswith("-i "):
        temp_text_b = message.caption.replace("-i ","")
        photo_file_id = message.photo[-1].file_id
        photo = await bot.get_file(photo_file_id)
        photo_path = photo.file_path
        await photo.download(photo_path)
        pil_image = Image.open(photo_path)
        img_plus_text_to_img(pil_image, temp_text_b, pipe_img_to_img)
        with open("C:/Users/aleks/Desktop/step2/output/img_to_img_w_txt.png", 'rb') as file:
            images_bytes_third = file.read()
        await bot.send_photo(chat_id=message.chat.id, photo=images_bytes_third, caption=f'Image generated using {temp_text_b} as a prompt and sent image as base', reply_markup=markup_idea_gen_e)
    elif "-c" in message.caption: 
        photo_file_id = message.photo[-1].file_id
        photo = await bot.get_file(photo_file_id)
        photo_path = photo.file_path
        await photo.download(photo_path)
        pil_image = Image.open(photo_path)
        img_to_palette(pil_image)
        with open("C:/Users/aleks/Desktop/step2/output/palette_donut.png", 'rb') as file:
            images_bytes_fourth = file.read()
        await bot.send_photo(chat_id=message.chat.id, photo=images_bytes_fourth, caption=f'Palette generated using sent image as base', reply_markup=markup_idea_gen_e)


#starting the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)