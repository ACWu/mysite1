from django.contrib import admin
from .models import ExpenseReport, ExpenseItem
from django.utils import timezone
from django.db import models
from django.forms.widgets import TextInput


# Register your models here.
class ExpenseItemInline(admin.TabularInline):
    model = ExpenseItem
    extra = 3

class SubmittedExpenseItemInline(ExpenseItemInline):
    model = ExpenseItem
    extra = 0
    readonly_fields = ('item_date','meals', 'hotel', 'telephone', 'transportation', 'misc','description',)
    can_delete = False
    
class ExpenseReportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['generate_date', 'submit_date']}),
        ('Company car mileage', {'fields': ['ending_mileage']}),
        ('Comment', {'fields': ['title'], 'classes': ['collapse']}),
    ]

    readonly_fields = ('generate_date', 'submit_date',)
    inlines = [ExpenseItemInline]
    other_set_of_inlines = [SubmittedExpenseItemInline]
    actions = None
    list_display = ('title', 'generate_date', 'submit_date', 'was_generated_recently')
    list_filter = ['generate_date']
    search_fields = ['title']
    formfield_overrides = {
        models.DecimalField: {'widget': TextInput(attrs={'class': 'text-right'})},
    }
    
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.generate_date = timezone.now()
            obj.added_by = request.user
        if '_save_submit' in  request.POST.keys():
            obj.submit_date = timezone.now()
        #obj.save()
        super().save_model(request, obj, form, change)
        
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
        
    def get_readonly_fields(self, request, obj=None):
        """
        Dynamically change read-only fields so that additional fields on submitted expense reports become read-only.
        """
        if obj:
            if obj.submit_date:
                return self.readonly_fields + ('ending_mileage', 'title',)
        return self.readonly_fields

    def get_inline_instances(self, request, obj=None):
        """
        Dynamically change inlines so that the inline expense items on submitted expense reports become read-only.
        """
        inline_instances = []

        if obj:
            if obj.submit_date:
                inlines = self.other_set_of_inlines
            else:
                inlines = self.inlines
                show_submit_button = True
        else:
            inlines = self.inlines
            show_submit_button = True
        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request) or
                        inline.has_change_permission(request) or
                        inline.has_delete_permission(request)):
                    continue
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)
        return inline_instances

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = ExpenseReport.objects.get(pk=object_id)
        if not obj.submit_date:
            extra_context = extra_context or {}
            extra_context['show_submit_button'] = True
        else:
            extra_context = extra_context or {}
            extra_context = {'show_save': False,
            'show_delete_link': False,        
            'show_save_as_new': True,    
            'show_save_and_continue': False,  
            'show_save_and_add_another': False,
            }
        return super().change_view(request, object_id, form_url, extra_context=extra_context)            

class Media:
    css = {

    }
admin.site.register(ExpenseReport, ExpenseReportAdmin)
admin.site.register(ExpenseItem)
admin.site.disable_action('delete_selected')