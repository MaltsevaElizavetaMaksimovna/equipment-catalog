from django.db import models


class Workshop(models.Model):
    """Цех"""
    name = models.CharField('Название цеха', max_length=200)
    code = models.CharField('Код цеха', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Цех'
        verbose_name_plural = 'Цеха'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Site(models.Model):
    """Площадка"""
    name = models.CharField('Название площадки', max_length=200)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, 
                                 verbose_name='Цех', related_name='sites')
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.workshop.code})"


class EquipmentType(models.Model):
    """Тип оборудования"""
    name = models.CharField('Название типа', max_length=200)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'
        ordering = ['name']

    def __str__(self):
        return self.name


class Equipment(models.Model):
    """Оборудование"""
    name = models.CharField('Название оборудования', max_length=300)
    inventory_number = models.CharField('Инвентарный номер', max_length=100, unique=True)
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT,
                                       verbose_name='Тип оборудования')
    site = models.ForeignKey(Site, on_delete=models.CASCADE,
                            verbose_name='Площадка', related_name='equipment')
    manufacturer = models.CharField('Производитель', max_length=200, blank=True)
    model = models.CharField('Модель', max_length=200, blank=True)
    serial_number = models.CharField('Серийный номер', max_length=200, blank=True)
    year = models.IntegerField('Год выпуска', null=True, blank=True)
    status = models.CharField('Статус', max_length=50, 
                             choices=[
                                 ('active', 'Работает'),
                                 ('maintenance', 'На обслуживании'),
                                 ('broken', 'Неисправно'),
                                 ('decommissioned', 'Списано'),
                             ], default='active')
    notes = models.TextField('Примечания', blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        ordering = ['inventory_number']

    def __str__(self):
        return f"{self.inventory_number} - {self.name}"


class EquipmentCharacteristic(models.Model):
    """Характеристика оборудования"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,
                                 related_name='characteristics',
                                 verbose_name='Оборудование')
    name = models.CharField('Название характеристики', max_length=200)
    value = models.CharField('Значение', max_length=500)
    unit = models.CharField('Единица измерения', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ['name']

    def __str__(self):
        unit_str = f" {self.unit}" if self.unit else ""
        return f"{self.name}: {self.value}{unit_str}"


class EquipmentDocument(models.Model):
    """Документ оборудования (паспорт, инструкция и т.д.)"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,
                                 related_name='documents',
                                 verbose_name='Оборудование')
    title = models.CharField('Название документа', max_length=300)
    file = models.FileField('Файл', upload_to='equipment_docs/')
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
