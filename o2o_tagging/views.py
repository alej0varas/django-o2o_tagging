from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import FormView

from .forms import TagFormAuthenticated
from .forms import TagFormAuthenticatedSet
from .signals import o2o_tags_created


class TagCreateView(FormView):
    form_class = TagFormAuthenticated

    def get_success_url(self):
        """Return a empty string to allow form_valid call to work"""
        return ''

    def form_valid(self, form):
        super(TagCreateView, self).form_valid(form)
        form.save(request=self.request)
        return HttpResponse(status=201)

    def form_invalid(self, form):
        return HttpResponseBadRequest()


class TagsCreateView(FormView):
    form_class = TagFormAuthenticatedSet

    def get_success_url(self):
        """Return a empty string to allow form_valid call to work"""
        return ''

    def form_valid(self, form):
        super(TagsCreateView, self).form_valid(form)
        tags = form.save(self.request)
        o2o_tags_created.send(self.__class__, instances=tags)
        return HttpResponse(status=201)

    def form_invalid(self, form):
        return HttpResponseBadRequest()
