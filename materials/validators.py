from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse


class YouTubeURLValidator:
    """
    Валидатор для проверки, что ссылка ведет на youtube.com.
    """

    message = _("Ссылка должна вести на youtube.com.")
    code = "invalid_youtube_url"

    def __call__(self, value):
        parsed_url = urlparse(value)
        if (
            "youtube.com" not in parsed_url.netloc
            and "youtu.be" not in parsed_url.netloc
        ):
            raise ValidationError(self.message, code=self.code)
