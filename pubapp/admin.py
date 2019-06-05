from django.contrib import admin

# Register your models here.
from pubapp.models import CharacterBio, Character, CharacterUser, StaticImage

admin.site.register(Character)
admin.site.register(CharacterBio)
admin.site.register(CharacterUser)
admin.site.register(StaticImage)
