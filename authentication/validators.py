from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from os.path import splitext

VALID_EXTENSIONS = ['.xlsx']

def validate_file_extension(value):
    try:
        ext = splitext(value.name)[1].lower()
        if ext not in VALID_EXTENSIONS:
            raise ValidationError(
            _('%(value)s is an invalid file type'),
            params={'value': value},
            )
        return value
    except:
        raise ValidationError(
            _('%(value)s is an invalid file type'),
            params={'value': value},
        )


VALID_EXTENSIONS_2 = ['.pdf']

MAX_SIZE = 4*1024*1024


def validate_file_extension_2(value):
    try:
        ext = splitext(value.name)[1].lower()
        if ext not in VALID_EXTENSIONS_2:
            raise ValidationError(
            _('%(value)s is an invalid file type'),
            params={'value': value},
            )
        return value
    except:
        raise ValidationError(
            _('%(value)s is an invalid file type'),
            params={'value': value},
        )



def validate_file_size(value):
    try:
        filesize = len(value)
        if filesize > MAX_SIZE:
            raise ValidationError(
                _('%(value)s file is loo large'),
                params={'value': value},
            )
    except:
        raise ValidationError(
            _('%(value)s file is loo large'),
            params={'value': value},
        )

SpecialSym =['$', '@', '#', '%', '!', '&', '^', '-', '_', '=', '+' ]


def validate_pw(pw):
    res = True
    if len(pw) < 8:
        res = False
        raise ValidationError(_("Password length should be at least 8 characters"), code=404)
    if not any(char.isdigit() for char in pw):
        res = False
        raise ValidationError("Password should contain atleast one number", code=404)
    if not any(char.isupper() for char in pw):
        res = False
        raise ValidationError("Password should contain at least one uppercase character", code=404)
    if not any(char.islower() for char in pw):
        print('Password should have at least one lowercase letter')
        res = False
        raise ValidationError("Password should contain at least one lowercase character", code=404)
    if not any(char in SpecialSym for char in pw):
        res = False
        raise ValidationError("Password should contain at least one special character", code=404)
    if res:
        return res

def validate_name(pw):
    res = True
    if any(char.isdigit() for char in pw):
        res = False
        raise ValidationError("Name should not contain numbers", code=404)
    if any(char in SpecialSym for char in pw):
        res = False
        raise ValidationError("Name should not contain special characters", code=404)
    if res:
        return res

def validate_phone_no(value):
    try:
        pass
    except Exception as e:
        print(e)