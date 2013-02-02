from django import forms

from .models import O2OTag


class BaseTagFormSet(forms.formsets.BaseFormSet):
    def save(self, request):
        tags = []
        for f in self.forms:
            tag = f.save(request=request)
            tags.append(tag.pk)
        tags = O2OTag.objects.filter(pk__in=tags)
        return tags


class TagFormAuthenticated(forms.ModelForm):
    def save(self, commit=True, request=None):
        tag = super(TagFormAuthenticated, self).save(commit=False)
        if hasattr(request, 'user') and request.user.is_authenticated():
            tagger = request.user
            tag.tagger_content_object = tagger
        if commit:
            tag.save()
        return tag

    class Meta:
        model = O2OTag
        exclude = ('tagger_content_type', 'tagger_object_id')


TagFormAuthenticatedSet = forms.formsets.formset_factory(
    TagFormAuthenticated,
    formset=BaseTagFormSet)
