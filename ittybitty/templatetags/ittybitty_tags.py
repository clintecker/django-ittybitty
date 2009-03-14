from django import template
from ittybitty.models import IttyBittyURL
from ittybitty.utils import gen_shortcut

register = template.Library()

class IttyBittyURLNode(template.Node):
    """
    Takes care of creating the actual Itty Bitty URL if one doesn't exist for
    the current page.  If one does exist already, it will be used.  If the tag
    was called with a "varname" parameter, the Itty Bitty URL object will be
    injected into the context using the value of "varname".  If no varname is
    specified, only the shortcut will be given to the template for rendering.
    """
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        request = context['request']

        # get the full URL for the current page
        url = request.build_absolute_uri()

        # see if it's worth shortening this URL
        path = request.path.strip('/')
        next_shortcut = gen_shortcut(IttyBittyURL.objects.count() + 1)

        # if we have a shortcut that matches the path, we shouldn't make an Itty Bitty URL
        if IttyBittyURL.objects.filter(shortcut__exact=path).count() or \
            len(path) <= len(next_shortcut):
            # it's shorter than the generated shortcut would be... don't store
            # the object and just use the URL itself
            ittybitty = IttyBittyURL(url=url, shortcut=path)
        else:
            # get the Itty Bitty URL object for this URL, and create one if one
            # doesn't already exist
            ittybitty, created = IttyBittyURL.objects.get_or_create(url=url)

        if self.varname:
            # if the user specified a varname, inject the object into the context
            context[self.varname] = ittybitty
            return ''
        else:
            # if no varname given, just spit the shortcut URL into the template
            return ittybitty.get_shortcut()

def ittybitty_url(parser, token):
    """
    Retrieves the Itty Bitty URL for the current page.

    Usage::

        Example 1::

            {% ittybitty_url as my_url %}
            <a href="{{ my_url.get_shortcut }}">Link to this page</a>

        Example 2::

            <a href="{{ ittybitty_url }}">Link to this page</a>
    """

    try:
        t, a, varname = token.split_contents()
    except ValueError:
        varname = None

    return IttyBittyURLNode(varname)

register.tag(ittybitty_url)
