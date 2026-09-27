from django.contrib import admin

# Register your models here.
from expense.models import Expenses,Employee
# Register your models here.
admin.site.register(Expenses)
admin.site.register(Employee)
    