from django import forms
from .models import Equipment, EquipmentType, Workshop


class EquipmentForm(forms.ModelForm):
    """Форма для добавления/редактирования оборудования"""
    
    class Meta:
        model = Equipment
        fields = [
            'name', 'inventory_number', 'equipment_type', 'site',
            'manufacturer', 'model', 'serial_number', 'year', 'status', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment_type': forms.Select(attrs={'class': 'form-control'}),
            'site': forms.Select(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EquipmentSearchForm(forms.Form):
    """Форма поиска оборудования"""
    search = forms.CharField(
        label='Поиск',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название, инвентарный номер, производитель...'
        })
    )
    equipment_type = forms.ModelChoiceField(
        label='Тип оборудования',
        queryset=EquipmentType.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    workshop = forms.ModelChoiceField(
        label='Цех',
        queryset=Workshop.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        label='Статус',
        choices=[('', 'Все')] + list(Equipment._meta.get_field('status').choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
