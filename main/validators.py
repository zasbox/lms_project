from rest_framework import serializers


class VideoURLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if "youtube.com" not in value[self.field]:
            raise serializers.ValidationError("Ссылка должна быть на видео в youtube")
