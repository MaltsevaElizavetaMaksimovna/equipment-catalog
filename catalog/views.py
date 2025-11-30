from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Equipment, EquipmentType, Workshop, Site
from .forms import EquipmentForm, EquipmentSearchForm


def index(request):
    """Главная страница"""
    equipment_count = Equipment.objects.count()
    type_count = EquipmentType.objects.count()
    workshop_count = Workshop.objects.count()
    
    context = {
        'equipment_count': equipment_count,
        'type_count': type_count,
        'workshop_count': workshop_count,
    }
    return render(request, 'catalog/index.html', context)


def equipment_list(request):
    """Список оборудования с поиском"""
    form = EquipmentSearchForm(request.GET)
    equipment = Equipment.objects.select_related(
        'equipment_type', 'site', 'site__workshop'
    ).prefetch_related('characteristics')
    
    # Поиск
    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        if search_query:
            equipment = equipment.filter(
                Q(name__icontains=search_query) |
                Q(inventory_number__icontains=search_query) |
                Q(manufacturer__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(serial_number__icontains=search_query) |
                Q(characteristics__value__icontains=search_query)
            ).distinct()
        
        equipment_type = form.cleaned_data.get('equipment_type')
        if equipment_type:
            equipment = equipment.filter(equipment_type=equipment_type)
        
        workshop = form.cleaned_data.get('workshop')
        if workshop:
            equipment = equipment.filter(site__workshop=workshop)
        
        status = form.cleaned_data.get('status')
        if status:
            equipment = equipment.filter(status=status)
    
    context = {
        'equipment_list': equipment,
        'form': form,
    }
    return render(request, 'catalog/equipment_list.html', context)


def equipment_detail(request, pk):
    """Детальная информация об оборудовании"""
    equipment = get_object_or_404(
        Equipment.objects.select_related('equipment_type', 'site', 'site__workshop')
        .prefetch_related('characteristics', 'documents'),
        pk=pk
    )
    context = {'equipment': equipment}
    return render(request, 'catalog/equipment_detail.html', context)


def equipment_create(request):
    """Добавление оборудования"""
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    
    context = {'form': form, 'title': 'Добавить оборудование'}
    return render(request, 'catalog/equipment_form.html', context)


def equipment_edit(request, pk):
    """Редактирование оборудования"""
    equipment = get_object_or_404(Equipment, pk=pk)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_detail', pk=pk)
    else:
        form = EquipmentForm(instance=equipment)
    
    context = {
        'form': form,
        'title': 'Редактировать оборудование',
        'equipment': equipment
    }
    return render(request, 'catalog/equipment_form.html', context)


def equipment_delete(request, pk):
    """Удаление оборудования"""
    equipment = get_object_or_404(Equipment, pk=pk)
    
    if request.method == 'POST':
        equipment.delete()
        return redirect('equipment_list')
    
    context = {'equipment': equipment}
    return render(request, 'catalog/equipment_confirm_delete.html', context)
