from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from store.models import Order,Orderitem
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template


'''function of order page ,in this page order history displayed'''
def index(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders':orders
        }
    return render(request,'store/orders/index.html',context)

'''Detailes of each order'''
def vieworder(request,t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = Orderitem.objects.filter(order=order)
    context = {
        'order':order,
        'orderitems':orderitems
        }
    return render(request,'store/orders/view.html',context)

'''invoice'''
def invoice(request,t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = Orderitem.objects.filter(order=order)
    context = {
        'order':order,
        'orderitems':orderitems
        }
    return render(request,'store/orders/invoice.html',context)
    
# '''Generation of pdf'''
# def generate_pdf(request):
#     pdf_buffer = io.BytesIO()
#     order = Order.objects.filter().filter(user=request.user).first()
#     orderitems = Orderitem.objects.filter(order=order)
#     # Create a HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="output.pdf"'

#     # Create a simple HTML template.
#     template = get_template('store/orders/invoice_pdf.html')
#     context = {
#         'order': order,
#         'orderitems': orderitems,
#     }
#     html = template.render(context)

#     # Generate the PDF from the HTML content.
#     pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

#     # Check if the PDF generation was successful.
#     if pisa_status.err:
#         return HttpResponse('PDF generation error', status=500)
#     pdf_buffer.seek(0)
#     response = HttpResponse(pdf_buffer, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="output.pdf"'
#     return response
def invoice_pdf(template_source,context_dict={}):
    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),result,encoding="utf-8",pagesize="A4",pagebreaks=False,)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type = "application/pdf")
    return None
    
def generate_pdf(request):
    order = Order.objects.filter(user=request.user).first()
    orderitems = Orderitem.objects.filter(order=order)
    
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    
    # pdf = invoice_pdf("store/orders/invoice_pdf.html")
    # return HttpResponse(pdf,content_type = "application/pdf")
    pdf = invoice_pdf("store/orders/invoice_pdf.html", context)
    return pdf
