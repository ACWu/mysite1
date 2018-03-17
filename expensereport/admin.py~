from django.contrib import admin
from .models import ExpenseReport, ExpenseItem

# Register your models here.
class ExpenseItemInline(admin.TabularInline):
    model = ExpenseItem
    extra = 3
    
class ExpenseReportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['generate_date']}),
        ('Ending mileage', {'fields': ['ending_mileage']}),
        ('Comment', {'fields': ['title'], 'classes': ['collapse']}),
    ]
    inlines = [ExpenseItemInline]
    list_display = ('title', 'generate_date', 'was_generated_recently')
    list_filter = ['generate_date']
    search_fields = ['generate_date']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        obj.save()
        
    def get_queryset(self, request):
        # If super-user, show all comments
        if request.user.is_superuser:
            return ExpenseReport.objects.all()
        return ExpenseReport.objects.filter(added_by=request.user)
        
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(ExpenseReportAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.added_by.id:
            return False
        return True

admin.site.register(ExpenseReport, ExpenseReportAdmin)
admin.site.register(ExpenseItem)