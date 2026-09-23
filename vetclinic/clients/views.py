from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from clients.models import Client
from clients.forms import ClientForm


class ClientListView(ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clients'
    paginate_by = 3
    ordering = ['surname']


    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return super().get_queryset().filter(
                        Q(surname__icontains=search) | Q(phone_number__icontains=search)
                    )
    

    def get(self, request):
        response = super().get(request)
        response.context_data['search'] = request.GET.get('search', '')

        return response


class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    template_name = 'clients/create.html'
    success_url = reverse_lazy('clients:list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'
    template_name = 'clients/update.html'
    success_url = reverse_lazy('clients:list')
    pk_url_kwarg = 'id'


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/delete.html'
    success_url = reverse_lazy('clients:list')
