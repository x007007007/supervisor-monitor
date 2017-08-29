from django.contrib import admin
from .models import Supervisor
from .models import SupervisorService
# Register your models here.

class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('url', 'identification')
    search_fields = ('url', 'identification')
    readonly_fields = ('identification', 'status')

    def action_shutdown(self, request, queryset):
        for item in queryset:
            item.shutdown()

    def action_reload(self, request, queryset):
        for item in queryset:
            item.reload()

    def action_restart(self, request, queryset):
        for item in queryset:
            item.restart()

    actions = ("action_reload", "action_restart", "action_shutdown")


class SupervisorServiceAdmin(admin.ModelAdmin):
    readonly_fields = ("name", "group", "supervisor", "status")
    list_display = ("name", "group", "supervisor", "status", "description")
    list_filter = ("supervisor", "group")
    search_fields = ("name", "supervisor__identification")

    def action_start(self, request, queryset):
        for item in queryset:
            item.start()

    def action_restart(self, request, queryset):
        for item in queryset:
            item.restart()

    def action_stop(self, request, queryset):
        for item in queryset:
            item.stop()

    actions = ("action_start", "action_restart", "action_stop")

admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(SupervisorService, SupervisorServiceAdmin)