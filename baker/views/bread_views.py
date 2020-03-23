from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import Bread
from ..forms import BreadForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import Http404


class BreadListView(ListView):
    model = Bread
    #template_name = "baker/bread_list.html"



class BreadDetailView(DetailView):
    model = Bread
    template_name = "baker/bread_detail.html"
    context_object_name = "bread"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(BreadDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(BreadDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(BreadDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(BreadDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(BreadDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(BreadDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(BreadDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(BreadDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(BreadDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(BreadDetailView, self).get_template_names()


class BreadCreateView(CreateView):
    model = Bread
    form_class = BreadForm
    # fields = ['title', 'text', 'description', 'geschnitten', 'created_date', 'published_date']
    template_name = "baker/bread_create.html"
    success_url = reverse_lazy("bread_list")

    def __init__(self, **kwargs):
        return super(BreadCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(BreadCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(BreadCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(BreadCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(BreadCreateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(BreadCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(BreadCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(BreadCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(BreadCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(BreadCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(BreadCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(BreadCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(BreadCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("baker:bread_detail", args=(self.object.pk,))


class BreadUpdateView(UpdateView):
    model = Bread
    form_class = BreadForm
    # fields = ['title', 'text', 'description', 'geschnitten', 'created_date', 'published_date']
    template_name = "baker/bread_update.html"
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "bread"

    def __init__(self, **kwargs):
        return super(BreadUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(BreadUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(BreadUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(BreadUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(BreadUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(BreadUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(BreadUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(BreadUpdateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(BreadUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(BreadUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(BreadUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(BreadUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(BreadUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(BreadUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(BreadUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(BreadUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(BreadUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("baker:bread_detail", args=(self.object.pk,))


class BreadDeleteView(DeleteView):
    model = Bread
    template_name = "baker/bread_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "bread"

    def __init__(self, **kwargs):
        return super(BreadDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(BreadDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(BreadDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(BreadDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(BreadDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(BreadDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(BreadDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(BreadDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(BreadDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(BreadDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(BreadDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse("baker:bread_list")
