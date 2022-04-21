from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_team_size(value):
    try:
        if value < 2:
            raise ValidationError(
                _('%(value) should be greater than 1'),
                params={'value': value},
            )
    except:
        raise ValidationError(
            _('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )