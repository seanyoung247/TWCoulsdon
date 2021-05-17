""" Generates pdf reports and tickets """
from __future__ import unicode_literals

import os
import segno

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import reverse
#from django.utils.text import slugify
from django.conf import settings

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration


def generate_ticket_pdf(request):
    """ Generates a pdf of the tickets in a given order
    """

    # Prepare the response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; test.pdf'

    # Construct the security check QR code as an svg data url for embedding
    qr_data = segno.make(
        request.build_absolute_uri(
            reverse('event_details', args=('and-then-there-were-none',))),
        micro=False
    ).svg_data_uri(scale=4)

    # Generate a html template for the ticket
    context = {
        'qr_data': qr_data,
        'template': {
            'image': '/media/tickets/test.jpg',
            'text_color': '#FFFFFF',
        },
        'event': {
            'title': 'Test Event'
        },
        'venue': {
            'name': 'Test Venue',
            'street_address1': 'Barrie Close',
            'street_address2': 'Chipstead Valley Road',
            'town_or_city': 'Coulsdon',
            'county': 'Surrey',
            'postcode': 'CR5 3BE',
        },

    }
    html = render_to_string('tickets/ticket.html', context)

    # Generate a pdf from the HTML
    font_config = FontConfiguration()
    HTML(string=html, base_url=request.build_absolute_uri()
        ).write_pdf(response, font_config=font_config)

    return response












