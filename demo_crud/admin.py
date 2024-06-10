from django.contrib import admin
from .all_models.users import CustomUser
from .all_models.work_management import CustomWorkManagement
from .all_models.jobs_management import CustomJobManagement

admin.site.register(CustomUser)
admin.site.register(CustomWorkManagement)
admin.site.register(CustomJobManagement)




# Register your models here.
