import os
import fitz
import PyPDF2
import requests
from PIL import Image, ImageDraw, ImageFont
import shutil


def concatenate_documents():
    pdf_writer = PyPDF2.PdfWriter()

    for file in get_file_list():
        with open('cache/' + file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
    with open('cache/result.pdf', 'wb') as output:
        pdf_writer.write(output)
    output.close()


def clear_cache():
    files = get_file_list()
    for file in files:
        os.remove('cache/' + file)


def get_file_list():
    filenames = []
    for filename in os.listdir('cache/'):
        if os.path.isfile(os.path.join('cache/', filename)):
            filenames.append(filename)
    return filenames


def download_image(url):
    response = requests.get(url, stream=True)
    with open('cache/img.png', 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
        file.close()

    from PIL import Image
    image = Image.open('cache/img.png')
    flipped_image = image.rotate(180)
    flipped_image.save('cache/img.png')

def create_image(text1, text2):
    width = 800
    height = 400
    background_color = (255, 255, 255)
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    font_size = 80
    font_color = (0, 0, 0)
    font_path = "font.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text1_width, text1_height = draw.textsize(text1, font=font)
    text1_x = (width - text1_width) // 2
    text1_y = (height - (text1_height * 2)) // 2
    text2_width, text2_height = draw.textsize(text2, font=font)
    text2_x = (width - text2_width) // 2
    text2_y = text1_y + text1_height
    draw.text((text1_x, text1_y), text1, font=font, fill=font_color)
    draw.text((text2_x, text2_y), text2, font=font, fill=font_color)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save("cache/img2.png")


def update_pdf(page):
    img_rect = fitz.Rect(460, -500, 910, -50)
    img_rect2 = fitz.Rect(120, -1800, 750, 500)
    img_rect3 = fitz.Rect(10, -500, 460, -50)
    document = fitz.open('cache/result.pdf')
    page = document[1 + page * 2]
    page.insert_image(img_rect, filename='cache/img.png')
    page.insert_image(img_rect2, filename='cache/img2.png')
    page.insert_image(img_rect3, filename='cache/qrcode.png')

    document.save('cache/result-2.pdf')
    document.close()
    shutil.move('cache/result-2.pdf', 'cache/result.pdf')
