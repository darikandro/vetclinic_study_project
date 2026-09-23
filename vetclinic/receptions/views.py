import calendar
from datetime import datetime, timedelta, time, date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from receptions.models import WorkingSlot, Booking, MedicalHistory
from doctors.models import Doctor
from clients.models import Client
from pets.models import Pet


def schedule(request):
    client_id = request.GET.get('client_id')
    pet_id = request.GET.get('pet_id')
    
    today = date.today()

    try:
        month = int(request.GET.get('month', today.month))
        year = int(request.GET.get('year', today.year))
    except ValueError:
        month = today.month
        year = today.year

    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    cal = calendar.Calendar(firstweekday=0)
    month_matrix = cal.monthdatescalendar(year, month)

    selected_doctor_id = request.GET.get('doctor')
    selected_date_str = request.GET.get('date')

    slots = None
    available_slots = None
    selected_date = None

    if selected_doctor_id and selected_date_str: 
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            slots = WorkingSlot.objects.filter(doctor_id=selected_doctor_id, # все рабочие слоты врача в выбранную дату
                                               date=selected_date).order_by('start')
            available_slots = slots.filter(is_available=True)
        except ValueError:
            pass

    working_days = None
    available_days = None
    nearest_slot = None
    if selected_doctor_id:
        working_days = WorkingSlot.objects.filter(    # все рабочие дни выбранного врача за текущий месяц
            doctor_id=selected_doctor_id,
            date__year=year,
            date__month=month
        ).values_list('date__day', flat=True).distinct() 

        available_days = WorkingSlot.objects.filter(    # рабочие дни с доступной записью
            doctor_id=selected_doctor_id,
            date__year=year,
            date__month=month,
            is_available=True
        ).values_list('date__day', flat=True).distinct() 

        nearest_slot = WorkingSlot.objects.filter(
            doctor_id=selected_doctor_id,
            is_available=True,
            date__gte=date.today()
        ).order_by('date', 'start').first()
        

    months_ru = [
        "", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    month_name = f"{months_ru[month]} {year}"
    

    context = {
        'doctors': Doctor.objects.all(), 
        'selected_doctor_id': int(selected_doctor_id) if selected_doctor_id else None,

        'month_matrix': month_matrix,
        'month_name': month_name,
        'working_days': working_days,
        'today_day': today.day if today.year == year and today.month == month else None,
        'year': year,
        'month': month,

        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,

        'available_days': available_days,
        'available_slots': available_slots,
        'slots': slots,
        'nearest_slot': nearest_slot,
        'selected_date': selected_date,

        'client_id': client_id,
        'pet_id': pet_id,
    }
    return render(request, 'receptions/schedule.html', context)


@staff_member_required
def schedule_create(request):
    doctors = Doctor.objects.all()
    
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        doctor = Doctor.objects.get(id=doctor_id)
        date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        start_time = request.POST.getlist('start_time')
        end_time = request.POST.getlist('end_time')

        if WorkingSlot.objects.filter(doctor=doctor, date=date).first():
            messages.error(request, 
                f'У {doctor} уже есть расписание на эту дату! Выберите другой день или перейдите во вкладку "изменить расписание"')

        else:
            for start, end in zip(start_time, end_time):
                current_time = datetime.strptime(start, '%H:%M')
                target_end = datetime.strptime(end, '%H:%M')
                while current_time < target_end:
                    slot_end = current_time + timedelta(minutes=30)
                    WorkingSlot.objects.create(doctor=doctor, date=date, start=current_time.time(), end=slot_end.time())
                    current_time = slot_end
            messages.success(request, f"Расписание для {doctor} на {date.strftime('%d.%m.%Y')} успешно добавлено!")
            

    context = {'doctors': doctors}

    return render(request, 'receptions/schedule_create.html', context)

@login_required
def confirm_booking(request):
    slot_id = request.GET.get('slot_id')
    slot = get_object_or_404(WorkingSlot, id=slot_id)

    if not slot.is_available:
        messages.error(request, 'К сожалению, это время уже занято. Выберите другое окно.')
        return redirect('receptions:schedule')

    if request.user.is_superuser:
        client_id = request.GET.get('client_id')
        client = get_object_or_404(Client, id=client_id)
    else:
        try:
            client = request.user.client_profile
        except AttributeError:
            messages.error(request, 'Перед записью необходимо связать аккаунт с карточкой клиники.')
            return redirect('accounts:profile', secure_id=request.user.secure_id.secure_id)

    pet_id = request.GET.get('pet_id')
    pet = None
    client_pets = None

    if pet_id:
        pet = get_object_or_404(Pet, id=pet_id)
    else:
        client_pets = Pet.objects.filter(owner=client)

    if request.method == 'POST':
        if not pet_id:
            selected_pet_id = request.POST.get('pet')
        else:
            selected_pet_id = pet_id
        
        if not selected_pet_id:
            messages.error(request, 'Пожалуйста, выберите питомца для записи.')
        else:
            Booking.objects.create(
                slot=slot,
                client=client,
                pet_id=selected_pet_id
            )
            
            slot.is_available = False
            slot.save()
            
            messages.success(request, 'Вы успешно записались на прием! Ждем вас в клинике.')
            
            # Перенаправляем в зависимости от прав
            if request.user.is_superuser:
                return redirect('receptions:schedule')
            return redirect('accounts:profile', secure_id=request.user.secure_id.secure_id)

    context = {
        'slot': slot,
        'client': client,
        'pet': pet,
        'client_pets': client_pets,
    }
    return render(request, 'receptions/confirm_booking.html', context)


@staff_member_required 
def select_client(request):
    slot_id = request.GET.get('slot_id')
    slot = get_object_or_404(WorkingSlot, id=slot_id)

    clients = Client.objects.all()
    
    context = {
        'slot': slot,
        'slot_id': slot_id,
        'clients': clients,
    }
    return render(request, 'clients/list.html', context)