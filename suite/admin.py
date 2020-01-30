from django.contrib.auth.admin import admin

from suite.models import Puppet


class MicroFrontendAdmin(admin.ModelAdmin):
    list_display = ["name", "route", "domain_url"]


admin.site.register(Puppet, MicroFrontendAdmin)