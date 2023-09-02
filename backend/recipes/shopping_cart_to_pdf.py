from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def generate_shopping_list_pdf(shopping_cart):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shop_сart.pdf"'
    buffer = BytesIO()
    pdfmetrics.registerFont(
        TTFont('Times-Roman', 'data/timesnewromanpsmt.ttf', 'UTF-8'))
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Times-Roman", 18)
    p.drawString(30, 700, "Список покупок:")
    x = 680
    for item in shopping_cart:
        p.drawString(30,
                     x,
                     f"{item['ingredient__name']}: "
                     f"{item['ingredient_sum']} "
                     f"{item['ingredient__measurement_unit']}.",)
        x -= 20
    p.showPage()
    p.save()
    file = buffer.getvalue()
    buffer.close()
    response.write(file)
    return response
