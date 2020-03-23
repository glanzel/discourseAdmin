from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import Cake
from ..forms import CakeForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import Http404


class CakeListView(ListView):
    model = Cake
    template_name = "baker/cake_list.html"
    paginate_by = 20
    context_object_name = "cake_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(CakeListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(CakeListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(CakeListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(CakeListView, self).get_queryset()

    def get_allow_empty(self):
        return super(CakeListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(CakeListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(CakeListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(CakeListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(CakeListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(CakeListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(CakeListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CakeListView, self).get_template_names()


class CakeDetailView(DetailView):
    model = Cake
    template_name = "baker/cake_detail.html"
    context_object_name = "cake"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(CakeDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(CakeDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(CakeDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(CakeDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(CakeDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(CakeDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(CakeDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(CakeDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(CakeDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CakeDetailView, self).get_template_names()


class CakeCreateView(CreateView):
    model = Cake
    form_class = CakeForm
    # fields = ['title', 'text', 'fruits', 'geschnitten', 'created_date', 'published_date']
    template_name = "baker/cake_create.html"
    success_url = reverse_lazy("cake_list")

    def __init__(self, **kwargs):
        return super(CakeCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(CakeCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(CakeCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(CakeCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(CakeCreateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(CakeCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(CakeCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(CakeCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(CakeCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(CakeCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(CakeCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(CakeCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CakeCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("baker:cake_detail", args=(self.object.pk,))


class CakeUpdateView(UpdateView):
    model = Cake
    form_class = CakeForm
    # fields = ['title', 'text', 'fruits', 'geschnitten', 'created_date', 'published_date']
    template_name = "baker/cake_update.html"
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "cake"

    def __init__(self, **kwargs):
        return super(CakeUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(CakeUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(CakeUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(CakeUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(CakeUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(CakeUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(CakeUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(CakeUpdateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(CakeUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(CakeUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(CakeUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(CakeUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(CakeUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(CakeUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(CakeUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(CakeUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CakeUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("baker:cake_detail", args=(self.object.pk,))


class CakeDeleteView(DeleteView):
    model = Cake
    template_name = "baker/cake_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "cake"

    def __init__(self, **kwargs):
        return super(CakeDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(CakeDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(CakeDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(CakeDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(CakeDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(CakeDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(CakeDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(CakeDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(CakeDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(CakeDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(CakeDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse("baker:cake_list")
