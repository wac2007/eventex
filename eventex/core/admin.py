from django.contrib import admin

# Register your models here.
from eventex.core.models import Speaker, Contact, Talk


class ContactInline(admin.TabularInline): #Criando a lista de contatos
    model = Contact
    extra = 1 #Quantidade de registros em branco


class SpeakerModelAdmin(admin.ModelAdmin):
    inlines = [ContactInline] # Assimilando a tabela de contato
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'photo_img', 'website_link']

    def website_link(self, obj):
        return '<a href="{0}">{0}</a>'.format(obj.website)

    website_link.allow_tags = True
    website_link.short_description = 'Website'

    def photo_img(self, obj):
        return '<img width="32px" src="{}" />'.format(obj.photo)

    photo_img.allow_tags = True
    photo_img.short_description = 'Foto'

admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk)