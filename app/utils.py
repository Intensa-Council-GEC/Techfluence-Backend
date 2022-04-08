from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import uuid

names = ["Atharv Parkhe", "Abhinav Borde", "Sairaj Rasam"]

# path = str(settings.BASE_DIR)+str(file)

font = ImageFont.truetype("font.ttf", 100)

# for i in names:
#     img = Image.open("certificate.jpg")
#     draw = ImageDraw.Draw(img)
#     draw.text(xy=(800, 630), text=i, fill=(0,0,0), font=font)
#     img.save("folder/" + i + " certificate" + ".jpg")