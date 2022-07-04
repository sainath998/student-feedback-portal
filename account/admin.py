from django.contrib import admin

from .models import (
    Student,
    Faculty,
)

# Admin Classes,

class StudentAdmin(admin.ModelAdmin) :

    def delete_model(self, request, obj) :
        print(f"delete_model on obj {obj}")

        print(f"obj user {obj.user}, student {obj.user.student}")

        # obj.user.student = None
        # obj.user.save()

        obj.user.delete()

        # print(f"after obj user {obj.user}, student {obj.user.student}")

        return super().delete_model(request, obj)


class FacultyAdmin(admin.ModelAdmin) :

    def delete_model(self, request, obj) :
        print(f"delete_model on obj {obj}")

        obj.user.delete()
        
        return super().delete_model(request, obj)





# Register your models here.
admin.site.register(Student, StudentAdmin)

admin.site.register(Faculty, FacultyAdmin)
