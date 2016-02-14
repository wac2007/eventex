from django.contrib import admin

# Register your models here.
from eventex.core.models import Speaker, Contact, Talk, Course


class ContactInline(admin.TabularInline): #Criando a lista de contatos
    model = Contact
    extra = 1 #Quantidade de registros em branco


class SpeakerModelAdmin(admin.ModelAdmin):
    inlines = [ContactInline] # Assimilando a tabela de contato
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'photo_img', 'website_link', 'email', 'phone']

    # ----------------------------------------------------------
    # Custom Fields
    # ----------------------------------------------------------

    def website_link(self, obj):
        return '<a href="{0}">{0}</a>'.format(obj.website)

    website_link.allow_tags = True #Permite o HTML
    website_link.short_description = 'Website'

    # ----
    def photo_img(self, obj):
        return '<img width="32px" src="{}" />'.format(obj.photo)

    photo_img.allow_tags = True
    photo_img.short_description = 'Foto'

    # ----
    def email(self, obj):
        return obj.contact_set.emails().first()

    # ----
    def phone(self, obj):
        return obj.contact_set.phones().first()

    phone.short_description = 'telefone'
    # ----------------------------------------------------------
    # ----------------------------------------------------------


class TalkModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(course=None)


# Register in admin
admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk, TalkModelAdmin)
admin.site.register(Course)