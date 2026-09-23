from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from pricelist.models import Service, ServiceCategory
from pricelist.forms import ServiceForm


def pricelist(request):
    services = Service.objects.all()
    categories = ServiceCategory.objects.all()

    selected_category_id = request.GET.get('category')

    if selected_category_id and selected_category_id != 'all':
        services = Service.objects.filter(category_id=selected_category_id)
    else:
        services = Service.objects.all()
        selected_category_id = 'all' 

    context = {
        'categories': categories,
        'services': services,
        'selected_category_id': selected_category_id,
    }
    return render(request, 'pricelist/pricelist.html', context)


@staff_member_required
def create(request):
    
    if request.method == "POST":
        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('pricelist:list')
    else:
        form = ServiceForm()
    return render(request, 'pricelist/create.html', {'form': form})


@staff_member_required
def edit(request, id):
    service = Service.objects.get(id=id)

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)

        if form.is_valid:
            form.save()
            return redirect('pricelist:list')
    else: 
        form = ServiceForm(instance=service)

    return render(request, 'pricelist/edit.html', {'form': form})


@staff_member_required
def delete(request, id):
    service = Service.objects.get(id=id)

    if request.method == "POST":
        service.delete()
        return redirect('pricelist:list')

    return render(request, 'pricelist/delete.html', {'service': service})      


@method_decorator(staff_member_required, name='dispatch')
class CategoryListView(ListView):
    model = ServiceCategory
    template_name = 'pricelist/categories/list.html'
    context_object_name = 'categories'


@method_decorator(staff_member_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = ServiceCategory
    template_name = 'pricelist/categories/create.html'
    success_url = reverse_lazy('pricelist:category_list')
    fields = "__all__"


@method_decorator(staff_member_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = ServiceCategory
    template_name = 'pricelist/categories/update.html'
    success_url = reverse_lazy('pricelist:category_list')
    fields = "__all__"


@method_decorator(staff_member_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = ServiceCategory
    template_name = 'pricelist/categories/delete.html'
    success_url = reverse_lazy('pricelist:category_list')
