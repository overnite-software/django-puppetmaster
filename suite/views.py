from django.http import Http404
from django.shortcuts import render, get_object_or_404
from bs4 import BeautifulSoup
import requests

from suite.models import Puppet


def build_link(url, tag, type):
    """
        Prepends a micro frontend domain url to the original
        absolute path

    :param url:
    :param tag:
    :param type:
    :return:
    """

    if tag[type].startswith('/'):
        tag[type] = f"{url}{tag[type]}"


def parse_descendants(url, descendants):
    """

        Checks the descendants of a tag from beautiful soup
        for and child with an href attribute or src attr and
        builds a link with the micro frontend domain

    :param url:
    :param descendants:
    :return:
    """
    for child in descendants:
        try:
            if child.has_attr('href'):
                build_link(url, child, 'href')
            if child.has_attr('src'):
                build_link(url, child, 'src')
        except AttributeError:
            pass


def puppet_view(request, route):
    """

    Based on the route, this view fetches the generated html
    file of a microfrontend such as React.js

    :param request:
    :param route:
    :return:
    """

    # Get list of available puppet routes and find the one that
    # is being requested.

    current_route = None
    puppet_routes = Puppet.objects.all().values('route')
    for puppet_route in puppet_routes:
        puppet_route_str = puppet_route['route']
        if route.find(puppet_route_str, 0, len(puppet_route_str)) >= 0:
            current_route = puppet_route_str

    if not current_route:
        raise Http404("Unable to locate route for application.")

    mf = get_object_or_404(Puppet, route=current_route)
    req = requests.get(f"{mf.domain_url}/{mf.html_file}")
    soup = BeautifulSoup(req.text, 'html.parser')
    parse_descendants(mf.domain_url, soup.head.contents)
    parse_descendants(mf.domain_url, soup.body.contents)

    return render(
        request,
        "puppet.html",
        {"react_index": {
            "body": soup.body.prettify(),
            "head": soup.head.prettify()
        }}
    )


def index(request):
    """
    Homepage of the django-microfrontend-suite
    :param request:
    :return:
    """

    return render(request, "index.html", {"micro_frontends": Puppet.objects.all()})
