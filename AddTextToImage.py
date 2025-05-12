from PIL import Image, ImageDraw, ImageFont

def add_text_to_panel(text, panel_image):
  text_image = generate_text_image(text, width = panel_image.width, height = panel_image.height)

  result_image = Image.new('RGB', (panel_image.width, panel_image.height + text_image.height))

  # Merge the panel image and text image
  result_image.paste(panel_image, (0, 0))
  result_image.paste(text_image, (0, panel_image.height))
  result_image.save("./test.jpg")
  return result_image

def generate_text_image(text, width = 1200, height = 120):
  # Required varaibles
  font = ImageFont.truetype(font="manga-temple.ttf", size=30)
  words = text.split()
  multiline_sentence = ""
  sentence = ""

  # Create a PIL drawing space
  image = Image.new('RGB', (width, height), color='white')
  draw = ImageDraw.Draw(image)
  max_width = 0
  # Loop over all the words in the sentence and if the sentence is longer than the text box place a \n and continue.
  for word in words:
    if draw.textlength(sentence + " " + word, font=font) > width:
      if max_width < draw.textlength(sentence + " " + word, font=font):
        max_width = draw.textlength(sentence + " " + word, font=font)
      multiline_sentence += sentence + "\n" 
      sentence = ""
    sentence += word  + " "
  x = -1* (width - max_width) // 2
  print(max_width)
  multiline_sentence += sentence
  draw.multiline_text((x, 0), multiline_sentence, fill=(0, 0, 0), font=font)
  return image

#add_text_to_panel("Hallo dit is een test. Dit bericht moet lang zijn om het te kunnen teseten en ik heb geen Lorum Ipsum generator hier momenteel. Mischien moet ik die maar eens downloaden.", Image.open("./TestingImage.jpg"))