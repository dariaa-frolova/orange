import sqlite3

print("Начало")
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Clothing_type (
  id_clothing_type INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  season TEXT NOT NULL CHECK (season IN ('Весна', 'Зима', 'Лето', 'Осень', 'Все'))
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Clothing_size (
  id_clothing_size INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  id_clothing_type INTEGER,
  FOREIGN KEY (id_clothing_type) REFERENCES Clothing_type(id_clothing_type) ON DELETE CASCADE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Position (
  id_position INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Employee (
  id_employee INTEGER PRIMARY KEY AUTOINCREMENT,
  lname TEXT NOT NULL,
  fname TEXT NOT NULL,
  mname TEXT,
  data_birth DATE NOT NULL,
  gender TEXT NOT NULL CHECK (gender IN ('М', 'Ж')),
  id_position INTEGER,
  id_shirt_size INTEGER,
  id_pants_size INTEGER,
  id_shoe_size INTEGER,
  status TEXT NOT NULL DEFAULT 'Работает' CHECK (status IN ('Работает', 'Уволен')),
  FOREIGN KEY (id_position) REFERENCES Position(id_position) ON DELETE SET NULL,
  FOREIGN KEY (id_shirt_size) REFERENCES Clothing_size(id_clothing_size) ON DELETE SET NULL,
  FOREIGN KEY (id_pants_size) REFERENCES Clothing_size(id_clothing_size) ON DELETE SET NULL,
  FOREIGN KEY (id_shoe_size) REFERENCES Clothing_size(id_clothing_size) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Clothing_requirements (
  id_clothing_requirement INTEGER PRIMARY KEY AUTOINCREMENT,
  id_position INTEGER NOT NULL,
  id_clothing_type INTEGER,
  quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
  FOREIGN KEY (id_position) REFERENCES Position(id_position) ON DELETE CASCADE,
  FOREIGN KEY (id_clothing_type) REFERENCES Clothing_type(id_clothing_type) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Clothing (
  id_clothing INTEGER PRIMARY KEY AUTOINCREMENT, 
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  id_clothing_type INTEGER NOT NULL,
  id_clothing_size INTEGER,
  price REAL NOT NULL,
  service_life TIMESTAMP,
  date_delivery TIMESTAMP,
  id_employee_del INTEGER,
  FOREIGN KEY (id_clothing_type) REFERENCES Clothing_type(id_clothing_type) ON DELETE RESTRICT,
  FOREIGN KEY (id_clothing_size) REFERENCES Clothing_size(id_clothing_size) ON DELETE SET NULL,
  FOREIGN KEY (id_employee_del) REFERENCES Employee(id_employee) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Addresses (
  id_address INTEGER PRIMARY KEY AUTOINCREMENT,
  city TEXT NOT NULL,
  street TEXT NOT NULL,
  house TEXT NOT NULL,
  apartament INTEGER CHECK(apartament > 0)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Warehouse (
  id_warehouse INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  id_address INTEGER,
  phone TEXT NOT NULL,
  FOREIGN KEY (id_address) REFERENCES Addresses(id_address) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Clothing_status (
  id_clothing_status INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Stock (
  id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
  id_warehouse INTEGER NOT NULL,
  id_clothing INTEGER NOT NULL,
  id_clothing_status INTEGER NOT NULL,
  note TEXT,
  FOREIGN KEY (id_warehouse) REFERENCES Warehouse(id_warehouse) ON DELETE RESTRICT,
  FOREIGN KEY (id_clothing) REFERENCES Clothing(id_clothing) ON DELETE RESTRICT,
  FOREIGN KEY (id_clothing_status) REFERENCES Clothing_status(id_clothing_status) ON DELETE RESTRICT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Suppliers (
  id_supplier INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  id_address INTEGER NOT NULL,
  phone TEXT NOT NULL,
  email TEXT NOT NULL,
  FOREIGN KEY (id_address) REFERENCES Addresses(id_address) ON DELETE RESTRICT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Request (
  id_request INTEGER PRIMARY KEY AUTOINCREMENT,
  name_clothing TEXT NOT NULL,
  amount INTEGER CHECK(amount > 0), 
  id_supplier INTEGER,
  id_employee INTEGER,
  date_request TIMESTAMP NOT NULL,
  id_warehouse INTEGER,
  FOREIGN KEY (id_supplier) REFERENCES Suppliers(id_supplier) ON DELETE SET NULL,
  FOREIGN KEY (id_employee) REFERENCES Employee(id_employee) ON DELETE SET NULL,
  FOREIGN KEY (id_warehouse) REFERENCES Warehouse(id_warehouse) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Issue (
  id_issue INTEGER PRIMARY KEY AUTOINCREMENT,
  id_employee INTEGER,
  id_stock INTEGER NOT NULL,
  id_iss_employee INTEGER,
  date_issue DATE NOT NULL,
  date_return DATE,
  note TEXT,
  FOREIGN KEY (id_employee) REFERENCES Employee(id_employee) ON DELETE SET NULL,
  FOREIGN KEY (id_stock) REFERENCES Stock(id_stock) ON DELETE CASCADE,
  FOREIGN KEY (id_iss_employee) REFERENCES Employee(id_employee) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Return_clothing (
  id_return INTEGER PRIMARY KEY AUTOINCREMENT,
  id_issue INTEGER NOT NULL,
  date_return DATE NOT NULL,
  note TEXT,
  FOREIGN KEY (id_issue) REFERENCES Issue(id_issue) ON DELETE CASCADE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Notification_type (
  id_notification_type INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Notifications (
  id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
  id_employee INTEGER,
  message TEXT NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_send TIMESTAMP,
  is_sent INTEGER NOT NULL DEFAULT 0,
  id_notification_type INTEGER,
  FOREIGN KEY (id_employee) REFERENCES Employee(id_employee) ON DELETE SET NULL,
  FOREIGN KEY (id_notification_type) REFERENCES Notification_type(id_notification_type) ON DELETE RESTRICT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Writting_off_reason (
  id_reason INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Writting_off (
  id_writting_off INTEGER PRIMARY KEY AUTOINCREMENT,
  id_clothing INTEGER,
  date_writting_off DATE NOT NULL,
  id_reason INTEGER,
  id_employee INTEGER,
  FOREIGN KEY (id_clothing) REFERENCES Clothing(id_clothing) ON DELETE SET NULL,
  FOREIGN KEY (id_reason) REFERENCES Writting_off_reason(id_reason) ON DELETE SET NULL,
  FOREIGN KEY (id_employee) REFERENCES Employee(id_employee) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Reservation (
  id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
  id_stock INTEGER,
  id_employee INTEGER NOT NULL,
  date_start DATE NOT NULL,
  date_end DATE NOT NULL,
  FOREIGN KEY (id_stock) REFERENCES Stock(id_stock),
  FOREIGN KEY (id_employee) REFERENCES Employee(id_employee) ON DELETE CASCADE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
  id_user INTEGER PRIMARY KEY AUTOINCREMENT,
  login TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  password_salt TEXT NOT NULL,
  id_employee INTEGER NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('Админ', 'Работник')),
  FOREIGN KEY (id_employee) REFERENCES Employee(id_employee) ON DELETE CASCADE
);
''')

conn.commit()

print("Вставка")
cursor.executescript("""

INSERT INTO Position (name) VALUES
('Токарь'),
('Фрезеровщик'),
('Сварщик'),
('Слесарь-ремонтник'),
('Электрик'),
('Кладовщик'),
('Контролер ОТК'),
('Инженер-технолог'),
('Бухгалтер'),
('Начальник цеха'),
('Начальник склада'),
('Сотрудник склада');
                     
INSERT INTO clothing_type("name", "season")
values ('Летний костюм', 'Лето'),
('Зимние штаны', 'Зима'),
('Летние штаны', 'Лето'),
('Демисезонные штаны', 'Весна'),
('Перчатки зимние', 'Зима'),
('Каска', 'Все'),
('Перчатки', 'Лето'),
('Куртка зимняя', 'Зима'),
('Футболка летняя', 'Лето'),
('Ботинки летние', 'Лето')
;

INSERT INTO clothing_size(name, id_clothing_type)
values ('54', 8),
('41', 9),
('42', 9),
('52-54', 7),
('54-56', 7),
('L', 6),
('M', 4),
('54', 1),
('56', 3),
('universal', 5);

INSERT INTO Employee (lname, fname, mname, data_birth, gender, id_position, id_shirt_size, id_pants_size, id_shoe_size, "status") 
VALUES
('Иванов', 'Иван', 'Иванович', '1985-05-10', 'М', 1, 8, 5, 9, 'Работает'),
('Петров', 'Петр', 'Петрович', '1990-08-15', 'М', 2, 8, 6, 10, 'Работает'),
('Сидоров', 'Сидор', 'Сидорович', '1978-02-20', 'М', 3, 8, 5, 9, 'Работает'),
('Смирнова', 'Елена', 'Алексеевна', '1982-11-01', 'Ж', 4, 8, 5, 9, 'Уволен'),
('Кузнецов', 'Дмитрий', 'Сергеевич', '1995-03-25', 'М', 5, 8, 6, 9, 'Работает'),
('Волкова', 'Ольга', 'Ивановна', '1988-06-05', 'Ж', 6, 8, 5, 9, 'Работает'),
('Соколов', 'Андрей', 'Викторович', '1975-09-12', 'М', 7, 8, 5, 10, 'Работает'),
('Лебедева', 'Татьяна', 'Михайловна', '1992-01-18', 'Ж', 8, 8, 6, 9, 'Работает'),
('Морозов', 'Сергей', 'Павлович', '1980-04-03', 'М', 12, 8, 5, 9, 'Работает'),
('Федорова', 'Наталья', 'Дмитриевна', '1987-07-30', 'Ж', 11, 8, 5, 10, 'Работает');

INSERT INTO Clothing_requirements (id_position, id_clothing_type, quantity) VALUES
(1, 1, 1), 
(1, 7, 2), 
(2, 1, 1),
(2, 7, 2), 
(3, 4, 1), 
(3, 8, 1), 
(4, 1, 1), 
(5, 1, 1), 
(6, 1, 1), 
(7, 1, 1); 

INSERT INTO Clothing (name, description, id_clothing_type, id_clothing_size, price, service_life, date_delivery, id_employee_del) VALUES
('Летний костюм "Стандарт"', 'Хлопковый костюм для общих работ', 1, 10, 2500, '2026-12-12', '2024-12-12', 9),
('Летняя куртка "Мастер"', 'Утепленная куртка для летних работ', 2, 7, 1800, '2026-12-12', '2024-12-12', 9),
('Брюки рабочие "Профи"', 'Усиленные брюки с карманами', 3, 2, 1200, '2026-12-12', '2024-12-12', 9),
('Зимний костюм "Арктика"', 'Теплый костюм для работы на улице', 4, 1, 6000, '2026-12-12', '2024-12-12', 9),
('Зимняя куртка "Север"', 'Куртка с меховым воротником', 5, 7, 4000, '2026-12-12', '2024-12-13', 9),
('Зимние брюки "Тайга"', 'Брюки с высокой спинкой', 6, 1, 2500, '2026-12-12', '2024-12-12', 9),
('Перчатки х/б', 'Стандартные рабочие перчатки', 7, 6, 100, '2025-06-12', '2024-12-12', 9),
('Шлем защитный', 'Ударопрочный шлем', 8, 5, 500, '2026-12-12', '2024-12-12', 9),
('Шапка зимняя', 'Теплая вязаная шапка', 9, 5, 300, '2026-12-12', '2024-12-12', 9),
('Ботинки рабочие', 'Кожаные ботинки с металлическим носком', 10, 9, 3500, '2026-12-12', '2024-12-13', 9);

INSERT INTO Addresses (city, street, house, apartament) VALUES
('Екатеринбург', 'Ленина', '10', 12),
('Екатеринбург', 'Малышева', '25', 34),
('Екатеринбург', 'Гагарина', '5', 56),
('Екатеринбург', 'Мира', '12', 78),
('Екатеринбург', 'Уральская', '8', 90),
('Екатеринбург', 'Белинского', '15', 123),
('Екатеринбург', 'Куйбышева', '3', 45),
('Екатеринбург', 'Луначарского', '20', 67),
('Екатеринбург', 'Тургенева', '7', 89),
('Екатеринбург', 'Шевченко', '11', 21);

INSERT INTO Warehouse (name, id_address, phone) VALUES
('Основной склад', 1, '89221234567'),
('Склад спецодежды', 2, '89221234568'),
('Склад инструментов', 3, '89221234569'),
('Склад материалов', 4, '89221234570');

INSERT INTO clothing_status (name)
values ('На складе'), ('Зарезервировано'), ('У сотрудника'), ('Списано'), ('В ремонте'), ('В химчистке'), ('Непригоден (списать)'), ('Нужен ремонт'), ('Нужна химчистка');

INSERT INTO Stock (id_warehouse, id_clothing, id_clothing_status) VALUES
(1, 1, 1),
(2, 2, 2),
(1, 3, 3),
(2, 4, 3),
(1, 5, 3),
(2, 6, 4),
(1, 7, 5),
(2, 8, 6),
(1, 9, 8),
(2, 10, 9);

INSERT INTO Suppliers (name, id_address, phone, email) VALUES
('ООО "Спецодежда"', 1, '89001112233', 'spec@mail.ru'),
('ООО "Текстиль"', 2, '89002223344', 'text@mail.ru'),
('ООО "Защита"', 3, '89003334455', 'zashita@mail.ru'),
('ООО "Инструмент"', 4, '89004445566', 'instr@mail.ru'),
('ООО "Обувь"', 5, '89005556677', 'obuv@mail.ru'),
('ООО "Снабженец"', 6, '89006667788', 'snab@mail.ru'),
('ООО "Костюм"', 7, '89007778899', 'kost@mail.ru'),
('ООО "Перчатка"', 8, '89008889900', 'perch@mail.ru'),
('ООО "Шлем"', 9, '89009990011', 'shlem@mail.ru'),
('ООО "Шапка"', 10, '89000001122', 'shapka@mail.ru');

INSERT INTO Request (name_clothing, amount, id_supplier, id_employee , date_request, id_warehouse) VALUES
('Куртка зимняя жен', 5, 1, 9, '2024-10-26 10:00:00', 1),
('Куртка летняя', 3, 2, 9, '2024-10-26 11:00:00', 1),
('Куртка зимняя', 2, 3, 9, '2024-10-26 11:00:00', 2),
('Костюм жен летний', 1, 4, 9, '2024-10-25 12:00:00', 2),
('Куртка зимняя', 4, 5, 9, '2024-10-26 13:00:00', 2),
('Перчатки', 6, 6, 9, '2024-10-20 14:00:00', 1),
('Куртка зимняя', 2, 7, 9, '2024-10-26 15:00:00', 1),
('Штаны зимние жен', 1, 8, 9, '2024-10-26 11:00:00', 2),
('Каска', 3, 9, 9, '2024-10-26 16:00:00', 1),
('Куртка зимняя муж', 5, 10, 9, '2024-10-20 17:00:00', 1);
                     
INSERT INTO Issue (id_employee, id_stock, id_iss_employee, date_issue, date_return, note) VALUES
(1, 1, 9,'2024-10-20', '2025-10-20', 'Для работы в цехе'),
(2, 2, 9,'2024-10-20', '2025-10-20', 'Для работы в цехе'),
(3, 3, 9,'2024-10-21', '2025-10-21', 'Для работы в цехе'),
(4, 4, 9,'2024-10-22', '2025-10-22', 'Для работы в цехе'),
(5, 5, 9,'2024-10-23', '2025-10-23', 'Для работы в цехе'),
(6, 6, 9, '2024-10-24', '2025-10-24', 'Для работы в цехе'),
(7, 7, 9, '2024-10-25', '2025-10-25', 'Для работы в цехе'),
(8, 8, 9, '2024-10-26', '2025-10-26', 'Для работы в цехе'),
(9, 9, 9, '2024-10-26', '2025-10-26', 'Для работы в цехе'),
(10, 10, 9, '2024-10-27', '2025-10-27', 'Для работы в цехе');

INSERT INTO Return_clothing (id_issue, date_return, note) VALUES
(1, '2025-10-20', 'Возврат после использования'),
(2, '2025-10-20', 'Возврат после использования'),
(3, '2025-10-21', 'Возврат после использования'),
(4, '2025-10-22', 'Возврат после использования'),
(5, '2025-10-23', 'Возврат после использования'),
(6, '2025-10-24', 'Возврат после использования'),
(7, '2025-10-25', 'Возврат после использования'),
(8, '2025-10-26', 'Возврат после использования'),
(9, '2025-10-26', 'Возврат после использования'),
(10, '2025-10-27', 'Возврат после использования');

insert into "notification_type" (name)
values ('Возврат спецодежды через 1 день'), ('Окончание резервирования одежды'), ('Возврат спецодежды сегодня'), ('Просрочен срок сдачи'), ('Увольнение сотрудника (сдача спецодежды)'), ('Новый сотрудник (выдать спецодежду)');

INSERT INTO Notifications (id_employee, message, date_created, date_send, is_sent, id_notification_type) VALUES
(1, 'Срок возврата спецодежды истекает', '2024-10-26 10:00:00', null, FALSE, 1),
(2, 'Срок возврата спецодежды истекает', '2024-10-26 11:00:00', null, FALSE, 1),
(3, 'Необходимо выдать спецодежду', '2024-10-26 12:00:00', null, FALSE, 6),
(4, 'Необходимо выдать спецодежду', '2024-10-26 13:00:00', null, FALSE, 6),
(5, 'Срок эксплуатации истекает', '2024-10-26 14:00:00', null, FALSE, 1),
(6, 'Срок эксплуатации истекает', '2024-10-26 15:00:00', null, FALSE, 1),
(7, 'Необходимо выдать спецодежду', '2024-10-26 16:00:00', null, FALSE, 6),
(8, 'Срок возврата спецодежды истекает', '2024-10-26 17:00:00', null, FALSE, 3),
(9, 'Срок возврата спецодежды истекает', '2024-10-26 18:00:00', null, FALSE, 3),
(10, 'Необходимо выдать спецодежду', '2024-10-26 19:00:00', null, FALSE, 6);

insert into reservation (id_stock, id_employee, date_start, date_end)
values (2, 3, '2024-10-26', '2025-10-26');

insert into writting_off_reason (name)
values ('Сотрудник не вернул'), ('Непригодное состояние'), ('Истечение срока эксплуатации');

insert into writting_off (id_clothing, date_writting_off, id_reason, id_employee)
values (6, '2024-10-26', 2, 10);
""")

conn.commit()
conn.close()

print("Все таблицы успешно созданы в database.db")