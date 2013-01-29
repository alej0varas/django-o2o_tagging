from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.views.generic import CreateView

from .models import O2OTag


class TagCreateView(CreateView):
    model = O2OTag

    def get_success_url(self):
        """Return a empty string to allow form_valid call to work"""
        return ''

    def form_valid(self, form):
        super(TagCreateView, self).form_valid(form)
        return HttpResponse(status=201)

    def form_invalid(self, form):
        return HttpResponseBadRequest()
