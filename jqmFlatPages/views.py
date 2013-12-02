import logging

from django.http import Http404
from django.shortcuts import render_to_response

from models import JqmFlatPage


logger = logging.getLogger('django.dev')

def page_detail(request, pk):
    """
    Retrieve, update or delete a comment instance.
    """
    try:
        page = JqmFlatPage.objects.get(pk=pk)
    except JqmFlatPage.DoesNotExist:
        raise Http404

    return render_to_response('jqmflatpage.html',{'page':page})

def page_for_id(request, pid):
    logger.debug(id)
    try:
        page = JqmFlatPage.objects.get(page_id=pid)
    except JqmFlatPage.DoesNotExist:
        raise Http404

    return render_to_response('jqmflatpage.html',{'page':page})