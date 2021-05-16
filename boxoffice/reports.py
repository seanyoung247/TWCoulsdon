""" Generates pdf reports and tickets """

from __future__ import unicode_literals

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.text import slugify

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration


def generate_ticket_pdf():
    """ Generates a pdf of the required tickets
    """
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; test.pdf"
    html = render_to_string("tickets/ticket.html")

    HTML(string=html).write_pdf(response)
    return response


#
# def donation_receipt(request, donation_id):
#     donation = get_object_or_404(Donation, pk=donation_id, user=request.user)
#     response = HttpResponse(content_type="application/pdf")
#     response['Content-Disposition'] =
#     "inline; filename={date}-{name}-donation-receipt.pdf".format(
#         date=donation.created.strftime('%Y-%m-%d'),
#         name=slugify(donation.donor_name),
#     )
#     html = render_to_string("donations/receipt_pdf.html", {
#         'donation': donation,
#     })
#
#     font_config = FontConfiguration()
#     HTML(string=html).write_pdf(response, font_config=font_config)
#     return response
