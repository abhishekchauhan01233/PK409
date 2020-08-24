from django.contrib import admin
from django.contrib.auth.models import Group
from .models import registrationdata, crop_farmer, farm_science_expert, machine_learning, feedback_model, contacts
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class registrationdata_Admin(ImportExportModelAdmin):
    list_display = ('region','first_name','last_name','aadhar','phone','email', )
    list_filter = ('region',)

class crop_farmer_Admin(ImportExportModelAdmin):
    exclude = ('user',)
    list_display = ('email','region','crop_name','crop_year','area','days','irrigation','fertilizers','pesticides','avg_temp','production','approval_status',)
    list_filter = ('region','crop_type','seed_type','crop_name',)

class farm_science_expert_Admin(ImportExportModelAdmin):
    exclude = ('user',)
    list_display = ('region','area','crop_name','seed_type','days','irrigation','fertilizers','pesticides','production',)
    list_filter = ('region','crop_type','seed_type','crop_name',)

class machine_learning_Admin(ImportExportModelAdmin):
    list_display = ('region','crop_name', 'crop_year','month','area','avg_temp','pressure','humidity','production',)
    list_filter = ('region','crop_type',)

class feedback_Admin(ImportExportModelAdmin):
    list_display = ('first_name','aadhar','phone','email','feedback',)

class contacts_Admin(ImportExportModelAdmin):
    list_display = ('serial_no', 'designation','name', 'mobile', 'email', 'address',)

admin.site.site_header = 'DOA Administration'
admin.site.index_title = 'DOA(Govt. of Bihar)'
admin.site.unregister(Group)

admin.site.register(registrationdata, registrationdata_Admin)
admin.site.register(crop_farmer, crop_farmer_Admin)
admin.site.register(farm_science_expert, farm_science_expert_Admin)
admin.site.register(machine_learning, machine_learning_Admin)
admin.site.register(feedback_model, feedback_Admin)
admin.site.register(contacts, contacts_Admin)