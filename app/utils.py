from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import uuid
from authentication.models import ParticipantsModel


def checkUser(email):
    try:
        if ParticipantsModel.objects.filter(email=email).exists():
            return True
        return False
    except Exception as e:
        print(e)

names = ["Atharv Parkhe", "Abhinav Borde", "Sairaj Rasam"]

# path = str(settings.BASE_DIR)+str(file)

font = ImageFont.truetype("font.ttf", 100)

# for i in names:
#     img = Image.open("certificate.jpg")
#     draw = ImageDraw.Draw(img)
#     draw.text(xy=(800, 630), text=i, fill=(0,0,0), font=font)
#     img.save("folder/" + i + " certificate" + ".jpg")


# image_1 = Image.open("1.webp")
# image_2 = Image.open("2.webp")
# image_3 = Image.open("3.webp")

# im_1 = image_1.convert('RGB')
# im_2 = image_2.convert('RGB')
# im_3 = image_3.convert('RGB')

# image_list = [im_2, im_3]

# im_1.save('my_images.pdf', save_all=True, append_images=image_list)