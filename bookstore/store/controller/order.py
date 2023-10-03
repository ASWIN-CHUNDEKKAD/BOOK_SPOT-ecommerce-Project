from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from store.models import Order,Orderitem
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from xhtml2pdf.default import DEFAULT_FONT
from reportlab.lib.pagesizes import letter  # Import the desired page size
from reportlab.lib.units import cm  # Import units (e.g., cm for margins)


# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile


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
    

'''GENERATION OF PDF'''
def invoice_pdf(template_source, context_dict={}):
    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, encoding="utf-8", pagesize="A4", pagebreaks=False)
    if not pdf.err:
        response = HttpResponse(content_type="application/pdf")
        # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        response.write(result.getvalue())
        return response
    return HttpResponse("PDF generation failed", content_type="text/plain")

def generate_pdf(request,t_no):
    # order = Order.objects.filter(user=request.user).first()
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = Orderitem.objects.filter(order=order)
    
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    
    pdf = invoice_pdf("store/orders/invoice_pdf.html", context)
    return pdf

    

        
        
        
        
                                                                                                                       