from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponsePermanentRedirect
from django.conf import settings
from ittybitty.models import IttyBittyURL

class IttyBittyURLMiddleware(object):
    """
    Handles redirecting users to the appropriate URL.  If a response object with
    an HTTP 404 status makes it to this middleware, it will check for any Itty
    Bitty URLs whose shortcuts match the requested path.  If a match is found,
    the hit count for the Itty Bitty URL is incremented and the user is
    redirected to the corresponding URL.  If no matching Itty Bitty URL is found
    the HTTP 404 will continue to bubble up.
    """
    def process_response(self, request, response):
        if response.status_code == 404:
            try:
                url = get_object_or_404(IttyBittyURL,
                                        shortcut__exact=request.path.strip('/'))
                url.hits += 1
                url.save()
                return HttpResponsePermanentRedirect(url.url)
            except Http404:
                return response
            except:
                if settings.DEBUG:
                    raise

        return response
