from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import UserSecureID
from pets.models import Pet
from pets.forms import PetClientForm
from clients.models import Client


def create(request, secure_id):
    id_object = get_object_or_404(UserSecureID, secure_id=secure_id)
    user = id_object.user
    client = Client.objects.filter(user_profile=user).first()

    form = PetClientForm()

    if request.method == 'POST':
        form = PetClientForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)  # Создаем объект питомца в памяти, но НЕ сохраняем в базу
            pet.owner = client
            pet.save()
            messages.success(request, f'Новый питомец успешно добавлен!')
            return redirect('accounts:profile', secure_id=secure_id)


    context = {'form': form}

    return render(request, 'pets/create.html', context)


def admin_create(request, id):
    client = get_object_or_404(Client, id=id)

    form = PetClientForm()

    if request.method == 'POST':
        form = PetClientForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)  # Создаем объект питомца в памяти, но НЕ сохраняем в базу
            pet.owner = client
            pet.save()
            messages.success(request, f'Новый питомец успешно добавлен!')
            return redirect('clients:list')


    context = {'form': form, 'client': client}

    return render(request, 'pets/create.html', context)


@staff_member_required
def admin_page(request, pet_id):
    pet = get_object_or_404(Pet.objects.select_related('owner'), id=pet_id)
    client = pet.owner

    slot_id = request.GET.get('slot_id')

    context = {
        'pet': pet,
        'client': client,
        'slot_id': slot_id,
    }
    return render(request, 'pets/admin_pet.html', context)
