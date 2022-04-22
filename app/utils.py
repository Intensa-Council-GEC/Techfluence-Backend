from authentication.models import ParticipantsModel
from PIL import Image, ImageDraw, ImageFont
from app.models import TeamEventModel
from django.conf import settings
from .threads import send_certificates


font = ImageFont.truetype("font.ttf", 100)


def checkUser(email):
    try:
        if ParticipantsModel.objects.filter(email=email).exists():
            return True
        return False
    except Exception as e:
        print(e)


def checkTeamEvent(org):
    try:
        if TeamEventModel.objects.filter(organiser=org):
            return True
        return False
    except Exception as e:
        print(e)


def generateCertificate(name, abc):
    try:
        img = Image.open("certificate.jpg")
        draw = ImageDraw.Draw(img)
        draw.text(xy=(800, 630), text=name, fill=(0,0,0), font=font)
        path = str(settings.BASE_DIR) + "/data/certificates/" + str(abc) + ".jpg"
        img.save(path)
        return str(path)
    except Exception as e:
        print(e)


def combineCertificates(imagelist, abc, email):
    try:
        images = [ Image.open(f) for f in imagelist ]
        pdf_path = str(settings.BASE_DIR) + "/data/print/" + str(abc) + ".pdf"
        images[0].save(
            pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
        )
        thread_obj = send_certificates(email, pdf_path)
        thread_obj.start()
    except Exception as e:
        print(e)
