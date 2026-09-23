from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from clients.models import Client
from accounts.models import UserSecureID
from clients.forms import ClientSearchForm, ClientCreationForm
from receptions.models import Booking, MedicalHistory


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Регистрация для {username} прошла успешно! Войдите в свой аккаунт. ')
            return redirect('accounts:login')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request, secure_id):
    id_object = get_object_or_404(UserSecureID, secure_id=secure_id)
    user = id_object.user
    client = Client.objects.filter(user_profile=user).first()

    search_form = ClientSearchForm()
    creation_form = ClientCreationForm()
    found_client = None
    search_performed = False                  # проверка, был ли осуществлен поиск

    if not client and request.method == 'POST': # обработка формы поиска клиента
        if 'search_submit' in request.POST:
            search_form = ClientSearchForm(request.POST)
            if search_form.is_valid():
                search_performed = True
                surname = search_form.cleaned_data['surname']
                phone = search_form.cleaned_data['phone_number']

                found_client = Client.objects.filter(surname__iexact=surname, phone_number = phone, user_profile__isnull = True).first()
                # iexact — поиск без учета регистра

        elif 'confirm_bind' in request.POST: # обработка подтвержения привязки юзера к клиенту
            client_id = request.POST.get('client_id')
            client_to_bind = Client.objects.filter(id=client_id, user_profile__isnull = True).first()
            if client_to_bind:
                client_to_bind.user_profile = user
                client_to_bind.save()
                messages.success(request, f'Привязка карточки клиента прошла успешно! ')
                return redirect('accounts:profile', secure_id=secure_id)

        elif 'create_client' in request.POST:
            creation_form = ClientCreationForm(request.POST)
            if creation_form.is_valid():
                creation_form.save()
                new_client_phone = creation_form.cleaned_data['phone_number']
                new_client = Client.objects.filter(phone_number = new_client_phone, user_profile__isnull = True).first()
                new_client.user_profile = user
                new_client.save()
                messages.success(request, f'Карточка клиента успешно создана! ')

                return redirect('accounts:profile', secure_id=secure_id)

    

    context = {'client': client, 
               'user': user, 
               'search_form': search_form, 
               'creation_form': creation_form,
               'found_client': found_client,
               'search_performed': search_performed}
    
    return render(request, 'accounts/profile.html', context)

@login_required
def visits(request, secure_id):
    id_object = get_object_or_404(UserSecureID, secure_id=secure_id)
    user = id_object.user
    client = Client.objects.filter(user_profile=user).first()

    pets = client.pets.all()
    pet_id = request.GET.get('pet')
    
    future_visits = Booking.objects.filter(client=client, status=Booking.Statuses.SCHEDULED)
    visit_history = MedicalHistory.objects.filter(visit__client=client, visit__status=Booking.Statuses.COMPLETED).all()
    if pet_id:
        visit_history = visit_history.filter(pet_id=pet_id)

    context = {
        "client": client,
        "pets": pets,
        "selected_pet_id": pet_id,
        "future_visits": future_visits,
        "visit_history": visit_history,
    }
    return render(request, 'accounts/my_visits.html', context)


@login_required
def visit_context(request, secure_id, visit_id):
    id_object = get_object_or_404(
        UserSecureID,
        secure_id=secure_id
    )

    user = id_object.user

    client = get_object_or_404(
        Client,
        user_profile=user
    )

    visit = get_object_or_404(
        Booking.objects.select_related(
            'slot__doctor',
            'pet',
            'client'
        ),
        id=visit_id,
        client=client
    )

    history = MedicalHistory.objects.filter(
        visit=visit
    ).first()

    context = {
        'visit': visit,
        'history': history,
        'client': client,
        'back_url': request.META.get(
            'HTTP_REFERER',
            '#'
        ),
    }

    return render(
        request,
        'accounts/visit_context.html',
        context
    )
