"""
functional_test.py
Functional tests for railsonwhite.com
"""
from http import HTTPStatus
from urllib.parse import urlunparse, urlparse
from xprocess import ProcessStarter
import requests
import pytest

url_conf = [
    ("http", "localhost:4000", HTTPStatus.OK),
#    ("http", "www.railsonwhite.com", HTTPStatus.OK),
#    ("http", "www.railsonwhite.com", HTTPStatus.FOUND),
#    ("https", "www.railsonwhite.com", HTTPStatus.OK),
#    ("http", "railson-white-partnership.github.io/website/", HTTPStatus.FOUND)
#    ("https", "railson-white-partnership.github.io/website/", HTTPStatus.OK)
]


paths = [
    "/",
    ]
"""
    "/approach/",
    "/client-list/",
    "/contact-us/",
    "/experience/",
    "/feed/",
    "/feed/atom/",
    "/feed/rss/",
    "/market-research/",
    "/our-work/",
    "/our-work/white-house-care/",
    "/our-work/adr-care/",
    "/our-work/ecca/",
    "/our-work/filmbank/",
    "/team/",
    "/wp-content/plugins/cforms/images/button-bg.gif",
    "/wp-content/plugins/cforms/js/cforms.js",
    "/wp-content/plugins/cforms/styling/calendar.css",
    "/wp-content/plugins/cforms/styling/captcha_reset_grey.gif",
    "/wp-content/plugins/cforms/styling/cforms.css",
    "/wp-content/plugins/cforms/styling/icon-alert.png",
    "/wp-content/plugins/cforms/styling/li-err-bg.png",
    "/wp-content/themes/default/assets/banner_top.gif",
    "/wp-content/themes/default/assets/greenband.gif",
    "/wp-content/themes/default/assets/right_panel_bg.gif",
    "/wp-content/themes/default/style.css",
    "/wp-content/uploads/2009/02/anglian-logo.png",
    "/wp-content/uploads/2009/02/care-agenda.jpg",
    "/wp-content/uploads/2009/02/ecca_casehistory.pdf",
    "/wp-content/uploads/2009/02/ecca-logo.jpg",
    "/wp-content/uploads/2009/02/ecca-web.jpg",
    "/wp-content/uploads/2009/02/filmbank-logo.jpg",
    "/wp-content/uploads/2009/02/hill-house.jpg",
    "/wp-content/uploads/2009/02/ken-and-chels-logo.png",
    "/wp-content/uploads/2009/02/radcliffes.png",
    "/wp-content/uploads/2009/02/st-nicks.jpg",
    "/wp-content/uploads/2009/02/whitehouse-web2.jpg",
    "/wp-content/uploads/2009/03/adr_casehistory.pdf",
    "/wp-content/uploads/2009/03/adr-st-nicholas-lets-talk2.jpg",
    "/wp-content/uploads/2009/03/adrcarelogo.jpg",
    "/wp-content/uploads/2009/03/filmbank.png",
    "/wp-content/uploads/2009/03/pdf_icon.thumbnail.jpg",
    "/wp-content/uploads/2009/03/pdf_icon.jpg",
    "/wp-content/uploads/2009/03/white-house-logo.png",
    "/wp-content/uploads/2009/03/whitehouse-video2.png",
    "/wp-content/uploads/2009/03/whitehouse-website.gif",
    "/wp-content/uploads/2011/01/adr-website.gif",
    "/wp-content/uploads/2011/01/adr_casehistory2.pdf",
    "/wp-content/uploads/2011/01/alistair_whitethumbnail2.jpg",
    "/wp-content/uploads/2011/01/ecca-bow-logo-small.jpg",
    "/wp-content/uploads/2011/01/ecca_casehistory.pdf",
    "/wp-content/uploads/2011/01/ecca-colour-main.jpg",
    "/wp-content/uploads/2011/01/ecca-home-page2.gif",
    "/wp-content/uploads/2011/01/ecca-opportunities-2011.png",
    "/wp-content/uploads/2011/01/filmbank_casehistory.pdf",
    "/wp-content/uploads/2011/01/mtg_logo_rgb.jpg",
    "/wp-content/uploads/2011/01/mtgcover2.jpg",
    "/wp-content/uploads/2011/01/rfts_logo_square_rgb.jpg",
    "/wp-content/uploads/2011/01/terry-melton.png",
    "/wp-content/uploads/2011/01/up-close-small-rgb.jpg",
    "/wp-content/uploads/2011/01/white-house_casehistory.pdf",
    "/wp-includes/wlwmanifest.xml",
    "/xmlrpc.php?rsd",
    "/xmlrpc.php",
]
"""

@pytest.fixture
def localserver(xprocess):
    class Starter(ProcessStarter):
        pattern = "Server running... press ctrl-c to stop."
        args = ["bundle", "exec", "jekyll", "serve"]
    logfile = xprocess.ensure("localserver", Starter)
    yield
    xprocess.getinfo("localserver").terminate()


@pytest.mark.parametrize("path", paths)
@pytest.mark.parametrize("scheme, netloc, status", url_conf)
def test_url_get(scheme, netloc, path, status, localserver):
    """Check URLs respond to HTTP requests."""
    params = query = fragment = ""
    components = scheme, netloc, path, params, query, fragment
    url = urlunparse(components)
    response = requests.get(url, allow_redirects=False)
    assert response.status_code == status

redirects = [
    ("railsonwhite.com", "www.railsonwhite.com"),
]

@pytest.mark.parametrize("source, target", redirects)
def test_url_get_found(source, target):
    """Check requests to apex domain redirect to subdomain."""
    scheme = "http"
    netloc = source
    path = "/"
    params = query = fragment = ""
    components = scheme, netloc, path, params, query, fragment
    url = urlunparse(components)
    response = requests.get(url, allow_redirects=False)
    assert response.status_code == HTTPStatus.FOUND
    assert "Location" in response.headers
    location = response.headers["Location"]
    parts = urlparse(location)
    assert parts.netloc == target
