import requests
import json
import base64

from django.template.loader import render_to_string
from requests import Response

from check.models import Check
from SheepFish_test.settings import (
    CHECK_CLIENT_TEMPLATE,
    CHECK_KITCHEN_TEMPLATE,
    WKHTMLTOPDF_URL,
)


def wkhtmltopdf_create_pdf_request(check: Check) -> Response:
    template = (
        CHECK_CLIENT_TEMPLATE
        if check.type == "Client"
        else CHECK_KITCHEN_TEMPLATE
    )
    check_html = render_to_string(template, {"check": check})
    b = base64.b64encode(bytes(check_html, "utf-8"))
    data = {
        "contents": b.decode("utf-8"),
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        WKHTMLTOPDF_URL, data=json.dumps(data), headers=headers
    )
    print(response)
    return response
