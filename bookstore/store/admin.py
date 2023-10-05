from django.contrib import admin
from . models import *
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# REPORT LAB LIBRARIES FOR GENERATING PDF
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import PageTemplate, BaseDocTemplate, Frame, Table
from reportlab.platypus.tables import TableStyle

# FUNCTION OF GENERATING PDF IN ADMIN SIDE
def generate_pdf(modeladmin, request, queryset, fields_to_include):
    model_name = modeladmin.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'

    # Creation of landscape A4-sized PDF document
    doc = BaseDocTemplate(response, pagesize=landscape(letter))

    # Creation of PageTemplate with a single Frame
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
    template = PageTemplate(frames=[frame])

    # Adding the PageTemplate to the document
    doc.addPageTemplates([template])

    elements = []

    data = [['S.No'] + [modeladmin.model._meta.get_field(field_name).verbose_name for field_name in fields_to_include]]

    for index, obj in enumerate(queryset.order_by('id'), start=1):
        data_row = [str(index)] + [str(getattr(obj, field_name)) for field_name in fields_to_include]
        data.append(data_row)

    # Defining custom styles for table borders
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Background color for the header row
        ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),  # Text color for the header row
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Border for all cells
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle vertical alignment for all cells
    ])

    table = Table(data)
    table.setStyle(table_style)

    elements.append(table)

    doc.build(elements)
    return response

generate_pdf.short_description = "Download selected items as PDF."

# CATEGORY
class CategoryAdmin(admin.ModelAdmin):
    
    def download_selected_pdf(self, request, queryset):
        # Define the fields you want to include in the PDF
        fields_to_include = ['id', 'name']
        return generate_pdf(self, request, queryset, fields_to_include)

    actions = [download_selected_pdf]

# PRODUCTS
class ProductAdmin(admin.ModelAdmin):
    
    def download_selected_pdf(self, request, queryset):
        # FIELDS THAT INCLUDES IN PDF
        fields_to_include = ['id', 'name','language','author','quantity']
        return generate_pdf(self, request, queryset, fields_to_include)

    actions = [download_selected_pdf]
    
# ORDER
class OrderAdmin(admin.ModelAdmin):
    
    def download_selected_pdf(self, request, queryset):
        # Define the fields you want to include in the PDF
        fields_to_include = ['id', 'fname','lname','phone','address','state','payment_mode','payment_id']
        return generate_pdf(self, request, queryset, fields_to_include)

    actions = [download_selected_pdf]
    

# ORDER ITEMS
class OrderitemAdmin(admin.ModelAdmin):
    
    def download_selected_pdf(self, request, queryset):
        # Define the fields you want to include in the PDF
        fields_to_include = ['id', 'order','product','price','quantity']
        return generate_pdf(self, request, queryset, fields_to_include)

    actions = [download_selected_pdf]
    
class CustomUserAdmin(UserAdmin):
    
    def download_selected_pdf(self, request, queryset):
        # Define the fields you want to include in the PDF
        fields_to_include = ['id', 'username', 'first_name', 'last_name', 'email']
        return generate_pdf(self, request, queryset, fields_to_include)

    actions = [download_selected_pdf]
admin.site.unregister(User)


# Register your models here.
admin.site.register(User, CustomUserAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)
admin.site.register(Orderitem,OrderitemAdmin)
admin.site.register(Profile)
admin.site.register(Banner)

