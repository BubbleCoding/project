from PIL import Image, ImageDraw, ImageFont
import sys
import json
import os

def add_text_to_panel(text, panel_image):
  text_image = generate_text_image(text,panel_image.width)
  
  result_image = Image.new('RGB', (panel_image.width, panel_image.height + text_image.height))

  result_image.paste(panel_image, (0, 0))

  result_image.paste(text_image, (0, panel_image.height))

  return result_image

def generate_text_image(text, width):
    # Define image dimensions
    width = width
    height = 128

    # Create a white background image
    image = Image.new('RGB', (width, height), color='white')

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Choose a font (Pillow's default font)
    font = ImageFont.truetype(font="manga-temple.ttf", size=30)

    # # Calculate text size
    text_width = draw.textlength(text, font=font)
    text_height = font.size

    # # Calculate the maximum font size that fits both width and height
    # max_font_size_width = width // len(text)
    # max_font_size_height = height

    # # Use the smaller of the two font sizes
    # font_size = min(max_font_size_width, max_font_size_height)

    # # Calculate the new text size
    # text_width, text_height = draw.textsize(text, font=font)

    # Calculate the position to center the text horizontally and vertically
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # Define text color (black in this example)
    text_color = (0, 0, 0)

    # Add text to the image
    draw.text((x, y), text, fill=text_color, font=font)

    return image

def load_data():
    with open("comic_book_script.json", "r") as file:
        data = json.load(file)
    return data

def load_text(i):
  data = load_data()
  panel_1_text = data['panels'][i]['text']
  return panel_1_text

def load_images():
    number_of_images = 6
    images_loaded = []
    images = os.listdir("./images/imagesWithoutText")
    for i in range(number_of_images):
        image = Image.open("./images/imagesWithoutText/" + images[i])
        images_loaded.append(image)
    return(images_loaded)

# def add_text_to_images():
#   for i in range(6):
#     images = load_images()
#     text = load_text(i)
#     image = images[i]
#     result = add_text_to_panel(text, image)
#     result.save("./images/imagesWithText/textAdded_" + str(i) + ".jpg")

def add_text_to_images(image, text, panel_number):
  #images = load_images()
  #text = load_text(i)
  #image = images[i]
  result = add_text_to_panel(text, image)
  result.save("./images/imagesWithText/textAdded_" + str(panel_number) + ".jpg")