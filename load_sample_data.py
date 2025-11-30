"""
Скрипт для загрузки примерных данных
Запуск: python manage.py shell < load_sample_data.py
"""

from catalog.models import Workshop, Site, EquipmentType, Equipment, EquipmentCharacteristic

# Создание цехов
if not Workshop.objects.exists():
    print("Создание цехов...")
    workshop1 = Workshop.objects.create(
        name="Механический цех",
        code="МЦ-01",
        description="Основной механический цех для токарных и фрезерных работ"
    )
    workshop2 = Workshop.objects.create(
        name="Сборочный цех",
        code="СЦ-01",
        description="Цех финальной сборки изделий"
    )
    workshop3 = Workshop.objects.create(
        name="Испытательная лаборатория",
        code="ИЛ-01",
        description="Лаборатория для тестирования и контроля качества"
    )
    print("✓ Цеха созданы")
else:
    print("Цеха уже существуют")
    workshop1 = Workshop.objects.get(code="МЦ-01")
    workshop2 = Workshop.objects.get(code="СЦ-01")
    workshop3 = Workshop.objects.get(code="ИЛ-01")

# Создание площадок
if not Site.objects.exists():
    print("\nСоздание площадок...")
    site1 = Site.objects.create(name="Токарный участок", workshop=workshop1)
    site2 = Site.objects.create(name="Фрезерный участок", workshop=workshop1)
    site3 = Site.objects.create(name="Участок сборки №1", workshop=workshop2)
    site4 = Site.objects.create(name="Участок сборки №2", workshop=workshop2)
    site5 = Site.objects.create(name="Измерительная лаборатория", workshop=workshop3)
    print("✓ Площадки созданы")
else:
    print("\nПлощадки уже существуют")
    site1 = Site.objects.first()
    site2 = Site.objects.all()[1] if Site.objects.count() > 1 else site1

# Создание типов оборудования
if not EquipmentType.objects.exists():
    print("\nСоздание типов оборудования...")
    type1 = EquipmentType.objects.create(
        name="Токарный станок",
        description="Станки для токарной обработки металлов"
    )
    type2 = EquipmentType.objects.create(
        name="Фрезерный станок",
        description="Станки для фрезерной обработки"
    )
    type3 = EquipmentType.objects.create(
        name="Измерительное оборудование",
        description="Приборы для контроля и измерений"
    )
    type4 = EquipmentType.objects.create(
        name="Сварочное оборудование",
        description="Оборудование для сварочных работ"
    )
    print("✓ Типы оборудования созданы")
else:
    print("\nТипы оборудования уже существуют")
    type1 = EquipmentType.objects.first()
    type2 = EquipmentType.objects.all()[1] if EquipmentType.objects.count() > 1 else type1

# Создание оборудования
if not Equipment.objects.exists():
    print("\nСоздание оборудования...")
    
    # Токарный станок 1
    eq1 = Equipment.objects.create(
        name="Токарный станок с ЧПУ HAAS ST-20",
        inventory_number="ТС-001",
        equipment_type=type1,
        site=site1,
        manufacturer="HAAS Automation",
        model="ST-20",
        serial_number="SN-2020-1234",
        year=2020,
        status="active",
        notes="Основной токарный станок для изготовления валов"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq1, name="Максимальный диаметр обработки", value="400", unit="мм"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq1, name="Длина обработки", value="600", unit="мм"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq1, name="Мощность шпинделя", value="15", unit="кВт"
    )
    
    # Токарный станок 2
    eq2 = Equipment.objects.create(
        name="Токарный станок 16К20",
        inventory_number="ТС-002",
        equipment_type=type1,
        site=site1,
        manufacturer="Завод им. Свердлова",
        model="16К20",
        serial_number="123456",
        year=2005,
        status="active"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq2, name="Диаметр обработки над станиной", value="400", unit="мм"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq2, name="РМЦ", value="1000", unit="мм"
    )
    
    # Фрезерный станок
    eq3 = Equipment.objects.create(
        name="Фрезерный станок DMG MORI DMU 50",
        inventory_number="ФС-001",
        equipment_type=type2,
        site=site2,
        manufacturer="DMG MORI",
        model="DMU 50",
        serial_number="DMU-2019-9876",
        year=2019,
        status="active",
        notes="5-осевой обрабатывающий центр"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq3, name="Количество осей", value="5", unit=""
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq3, name="Размер стола", value="500x500", unit="мм"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq3, name="Максимальная скорость шпинделя", value="12000", unit="об/мин"
    )
    
    # Станок на ремонте
    eq4 = Equipment.objects.create(
        name="Токарный станок 1К62",
        inventory_number="ТС-003",
        equipment_type=type1,
        site=site1,
        manufacturer="Завод им. Свердлова",
        model="1К62",
        year=1998,
        status="maintenance",
        notes="На капремонте. Ожидается замена шпинделя"
    )
    
    # Измерительное оборудование
    eq5 = Equipment.objects.create(
        name="Координатно-измерительная машина",
        inventory_number="ИО-001",
        equipment_type=type3,
        site=site5,
        manufacturer="Zeiss",
        model="Contura G2",
        serial_number="ZS-2021-5555",
        year=2021,
        status="active"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq5, name="Диапазон измерения X", value="700", unit="мм"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq5, name="Диапазон измерения Y", value="1000", unit="мм"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq5, name="Диапазон измерения Z", value="600", unit="мм"
    )
    EquipmentCharacteristic.objects.create(
        equipment=eq5, name="Точность", value="2.2 + L/350", unit="мкм"
    )
    
    print("✓ Оборудование создано")
    print(f"\nСоздано единиц оборудования: {Equipment.objects.count()}")
else:
    print("\nОборудование уже существует")

print("\n" + "="*50)
print("✓ ПРИМЕРНЫЕ ДАННЫЕ ЗАГРУЖЕНЫ")
print("="*50)
print("\nТеперь вы можете:")
print("1. Перейти на главную страницу: http://127.0.0.1:8000/")
print("2. Просмотреть каталог: http://127.0.0.1:8000/equipment/")
print("3. Войти в админку: http://127.0.0.1:8000/admin/ (admin/admin123)")
