import telebot
from telebot import types

import mysql.connector
from mysql.connector import Error
import time

# Данный бот работает с базой SQl и решает проблему малого и среднего бизнеса, учета рабочего времени сотрудника.
# У каждого сотрудника есть свой индивидуальное "имя" в БД.
# Введется учет когда приступил к работе, когда закончил и общее время работы
# Метка "начало","конец" производится в чате бота
# Руководитель может добавлять, удалять сотрудника.Просматривать таблицу

app = telebot.TeleBot("5525289920:AAGB1AFCU-n8W9aPJ-V06HJNqZl_JgmLJIk")
#1.Напиши /bd для проверки БД
#2.Создание аккаунта руководителя(Создание новой БД с таблицей)(/new_supervisor)
#3.Подключение акк сотрудника (worker)



print('БОТ работает')

@app.message_handler(commands=['start'])
def go(message):
    global tg
    tg = zaebalo(message.chat.username,message.chat.id )
    app.send_message(message.chat.id, time.strftime('%d %m %y'))
    app.send_message(message.chat.id, 'Нажми /go для начала работы')

@app.message_handler(commands=['go'])
def start(message):
    app.send_message(message.chat.id, """Это telegram bot SQL
        1.Проверить уже созданную базу данных -- /bd --
        2.Создать новую базу данных и таблицу -- /new_supervisor --
        3.Подключение сотрудника к базе данных -- /worker --
        """)

@app.message_handler(commands=['bd'])
def bd(message):
    app.send_message(message.chat.id, "Напиши пароль")
    app.register_next_step_handler(message, one)

def one(message):
    global password_text
    password_text = message.text
    app.send_message(message.chat.id, f"ты ввел {password_text}  Началась проверка....")
    tg.on_off(password_text)
@app.message_handler(commands=['table'])
def con_table(message):
    app.send_message(message.chat.id, "Напиши название таблицы без спецальных символов")
    app.register_next_step_handler(message, con_table1)
def con_table1(message):
    new_table_text = message.text
    tg.check_table(new_table_text)

@app.message_handler(commands=['table_worker'])
def worker_table(message):
    app.send_message(message.chat.id, "Напиши название таблицы без спецальных символов")
    app.register_next_step_handler(message, worker_table2)
def worker_table2(message):
    new_table_text = message.text
    tg.check_table_worker(new_table_text)

@app.message_handler(commands=['new_supervisor'])
def new_supervisor(message):
    app.send_message(message.chat.id, "Будет созданна база данных с таблицей, которая будет доступна только вам и в дальнейшем будете взаимодействовать с ней. !!!Пароль не может начинаться с цифры!!!")
    app.send_message(message.chat.id, "Придумай пароль для БД")
    app.register_next_step_handler(message, wirra)
    text = message.text
    print(text)
def wirra(message):
    global text_table
    text_table = message.text
    app.send_message(message.chat.id, "Придумай название таблицы")
    app.register_next_step_handler(message, wirra2)

def wirra2(message):
    text1 = message.text
    tg.new_supervisor_2(text_table, text1)

@app.message_handler(commands=['worker'])
def worker(message):
    app.send_message(message.chat.id, "Пришли номер который тебе выслал твой руководитель")
    app.register_next_step_handler(message, numb)
def numb(message):
    text = message.text
    tg.connect_worker(text)
@app.message_handler(commands=['sonya'])
def sonya(message):
    for i in range(100):
        app.send_message(message.chat.id, "Я Люблю Соню!")


class New():
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.ruk = None
        self.wor = None
        self.u_bd = None
        self.connection = None
        self.table_name = None

        print(self.name, self.id)

    #Подключение к БД SQL
    def con(self, user_host, user_user, user_password, user_bd):
        connection = None
        try:
            connection = mysql.connector.connect(
                host = user_host,
                user = user_user,
                password = user_password,
                database = user_bd
            )
            self.ruk = 1
            self.wor = 0
            app.send_message(self.id, "Подключение прошло успешно, Нажми чтобы ввести название таблицы /table  ")
            self.u_bd = user_bd
            self.connection = connection
            print('pas', self.u_bd, 'table', self.table_name)

            return connection

        except Error as e:
            print('Ошибка')
            app.send_message(self.id, "База не найдена, повторить?  /yes  /not ")

            @app.message_handler(commands=['yes'])
            def bd(message):
                app.send_message(message.chat.id, "Проверь и напиши пароль")
                app.register_next_step_handler(message, one)

            def one(message):
                text = message.text
                app.send_message(message.chat.id, f"ты ввел {text}  Началась проверка....")
                tg.on_off(text)

            @app.message_handler(commands=['not'])
            def no(message):
                start(message)

#Проверяем зарегистрированный ли руководитель в БД или нет
    def on_off(self, text):
        self.text = text
        bd = str(self.id) + self.text
        print("тут работает")
        connection = tg.con('localhost', 'root', 'root', bd)


    #Создание БД
    def newbd(self):
        try:

            connection = mysql.connector.connect(
                host= 	'localhost',
                user = "root",
                password = 'root'

            )
            return connection
        except Error as e:
            print(e)
            app.send_message(self.id, "Произошла ошибка, нажми /new_supervisor чтобы попробовать еще раз.")


    #создание таблицы
    def newbd_2(self, name_bd):
        try:
            connection = mysql.connector.connect(
                host= 	'localhost',
                user = "root",
                password = 'root',
                database = name_bd

            )
            print('Успешно')
            return connection
        except Error as e:
            print(e)
            app.send_message(self.id, "Произошла ошибка, нажми /new_supervisor чтобы попробовать еще раз.")


    def zxc(self, text):
        self.table_name = text
        print(self.table_name)
        print(self.pass_text)
        try:
            table = "CREATE TABLE " + str(self.table_name) +" (ID INT NOT NULL AUTO_INCREMENT,login_telegram VARCHAR(20) NOT NULL, name VARCHAR(20) NOT NULL,data VARCHAR(20), time_start VARCHAR(9), time_end VARCHAR(9), time_total VARCHAR(12), commentar TEXT,   PRIMARY KEY(ID)) "+";"
            con_table = self.newbd_2(self.name_bd)
            qqq = con_table.cursor()
            qqq.execute(table)
            con_table.commit()
            qqq.close()
            print('создание Таблицы законченно')
            app.send_message(self.id, "Создание прошло успешно!")
            app.send_message(self.id, f"Пароль от БД - {self.pass_text} -")
            app.send_message(self.id, f"Название таблицы в БД - {self.table_name} -")
            app.send_message(self.id, f"Это ваш индивидуальный индификатор, через который сотрудники могут подключаться к базе - {self.id} -")
            app.send_message(self.id, "Нажми /bd для подключения")
        except Error as e:
            print(e)
            app.send_message(self.id, "Произошла ошибка, нажми /new_supervisor чтобы попробовать еще раз.")

    def new_supervisor_2(self, pass_text, table_text):
        print(pass_text, table_text)
        self.pass_text = pass_text
        x = table_text
        try:
            self.name_bd = str(self.id) + self.pass_text
            bd = "CREATE DATABASE " + self.name_bd + ";"
            con2 = self.newbd()
            con1 = con2.cursor()
            con1.execute(bd)
            con1.close()
            print('База созданна')
            self.zxc(x)
        except Error as e:
            print(e)
            app.send_message(self.id, "Произошла ошибка, вероятно база данных с таким паролем уже созданна.")
            app.send_message(self.id, "Нажми /new_supervisor чтобы попробовать еще раз.")
            app.send_message(self.id, "Нажми /start чтобы вернукться в главное меню")

    def check_worker(self):
        try:

            connection = mysql.connector.connect(
                host= 	'localhost',
                user = "root",
                password = 'root'

            )
            return connection
        except Error as e:
            print(e)
            app.send_message(self.id, "Ошибка. Не найдено. Попробовать еще раз /worker")
            app.send_message(self.id, "Вернуться в главное меню /start")


    #Проверка и подключение сотрудника к БД
    def connect_worker(self, text_):
        text = str(text_)
        text = text.lower()
        show_bd = "SHOW DATABASES;"
        connection = self.check_worker()
        con = connection.cursor()
        con.execute(show_bd)
        x = con.fetchall()
        print(type(x))
        print(x)
        for i in x:
            print(i)
            word = str(i)
            if text in word:
                self.wor = 1
                self.ruk = 0
                import re
                w = re.sub("[(|,|)|']", "", word)
                print(w)
                connection = tg.con('localhost', 'root', 'root', w)
                app.send_message(self.id, "Подключено. Нажми и введи название таблицы /table_worker")

    def check_table_worker(self, text_):
        text = str(text_)
        text = text.lower()
        show_bd = "SHOW TABLES;"
        con = self.connection.cursor()
        con.execute(show_bd)
        x = con.fetchall()
        for i in x:
            word = str(i)
            print(word, '>', text)
            if text in word:
                app.send_message(self.id, "Такая таблица есть.")
                app.send_message(self.id, "Отлично. Теперь можешь перейти в панель управления. Нажми /fellow_worker")
                self.table_name = text
            else:
                print("Error table")
                # обработать ошибку

    def check_table(self, text_):
        text = str(text_)
        text = text.lower()
        show_bd = "SHOW TABLES;"
        con = self.connection.cursor()
        con.execute(show_bd)
        x = con.fetchall()
        for i in x:
            word = str(i)
            print(word, '>', text)
            if text in word:
                app.send_message(self.id, "Такая таблица есть.")
                app.send_message(self.id, "Отлично. Теперь можешь перейти в панель управления. Нажми /supervisor")
                self.table_name = text
            else:
                print("Error table")
                #обработать ошибку








#ДОБАВИТЬ СОЗДАНИЕ НОВОЙ ТАБЛИЦЫ(ПОТОМ)
#Добавлять новых сотрудников
#Просматривать всю информацию
#Удалять сотрудников
#Просмотр времени сотрудника (|дата|начало работы|конец работы|(в конце списка общее время)) < сюда добавить фильтр даты 'от' и 'до'
#Просмотр конкретного сотрудника
@app.message_handler(commands=['supervisor'])
def supervisor1(message):
    global sv
    sv = Supervisor(message.chat.username, message.chat.id)
@app.message_handler(commands=['add'])
def add(message):
    app.send_message(message.chat.id, """Введи логин и имя сотрудника.
    Пример: login,Имя Фамилия
    После запятой не ставить пробел и в конце не ставить точку""")
    app.register_next_step_handler(message, add2)
def add2(message):
    text = message.text
    app.send_message(message.chat.id, f"ты ввел {text} ")
    sv.add(text)
@app.message_handler(commands=['watch'])
def qwe(message):
    sv.watch()
@app.message_handler(commands=['delete'])
def delete(message):
    app.send_message(message.chat.id, "Напиши логин телеграмм сотрудника. ВНИМАНИЕ ВОССТАНОВИТЬ ДАННЫЕ НЕ ПОЛУЧИТСЯ")
    app.register_next_step_handler(message, delete2)
def delete2(message):
    text = message.text
    app.send_message(message.chat.id, f"ты ввел {text} ")
    sv.dell(text)
@app.message_handler(commands=['view'])
def view(message):
    app.send_message(message.chat.id, "Просмотр времени работы от даты  и до другой даты")
    app.send_message(message.chat.id, "Напиши от какой даты ты хочешь посмотреть. Пример записи '02.06=08.06=login_telegram'")
    app.register_next_step_handler(message, num)
def num(message):
    text = message.text
    app.send_message(message.chat.id, f"Ты введ text={text}")
    sv.view(text)




class Supervisor(New):
    def __init__(self, name, id):
        super().__init__(name, id)
        self.wor = tg.wor
        self.u_bd = tg.u_bd
        self.connection = tg.connection
        self.ruk = tg.ruk
        self.table_name = tg.table_name
        print(self.id, self.wor,self.ruk,self.name)
        app.send_message(self.id, f"{self.id}, {self.wor},{self.ruk},{self.name},{self.u_bd}, {self.connection}")
        app.send_message(self.id, '''
            1.Добавить нового сотрудника --/add--
            2.Удалить сотрудника --/delete--
            3.Просмотр таблицы --/watch--
            4.Просмотр определенного промежутка времени --/view--()

            ''')

    #Выгрузка данных из таблицы
    def watch(self):
        if self.ruk == 1:
            try:
                request = 'SELECT * FROM ' +self.table_name + ";"
                watch1 = self.connection.cursor()
                watch1.execute(request)
                z = watch1.fetchall()
                for i in z:
                    print(i)
                    app.send_message(self.id, f'id={i[0]}, login={i[1]}, name={i[2]},num={i[3]},num={i[4]},num={i[5]},num={i[6]}')
            except BaseException as e:
                print(e)
                app.send_message(self.id, "Ошибка вернись /start")
    #Добавление нового сотрудника
    def add(self, text):
        if self.ruk == 1:
            try:
                log_name = text.split(',')
                request = f'INSERT INTO {self.table_name}(`login_telegram`,`name`) VALUES ("{str(log_name[0])}", "{str(log_name[1])}");'
                watch1 = self.connection.cursor()
                watch1.execute(request)
                self.connection.commit()
                app.send_message(self.id, f"Ты добавил login={str(log_name[0])}, Name={str(log_name[1])}")
                print('Удачно', log_name)
            except Error as e:
                print('Ошибка' + e)
    #Удаление сотрудника по id
    def dell(self, text):
        try:
            request = f'DELETE FROM {self.name} WHERE login_telegram ={str(text)};'
            watch1 = self.connection.cursor()
            watch1.execute(request)
            self.connection.commit()
            app.send_message(self.id, f"Удален login={text}")
            print('Удалено', text)
        except Error as e:
            print('Ошибка')
#выгружает данны условие дата от и до
    def view(self, text):
        date_2 = text.split('=')
        user = str(date_2[2])
        number_start = date_2[0].split('.')
        number_end = date_2[1].split('.')
        number_start = int(number_start[0])+int(number_start[1])
        number_end = int(number_end[0]) + int(number_end[1])
        try:
            request = f"SELECT * FROM {self.table_name} WHERE login_telegram = '{user}' ;"
            watch1 = self.connection.cursor()
            watch1.execute(request)
            z = watch1.fetchall()
            for i in z:
                date = i[3].split('/')
                num_date = int(date[0])+int(date[1])
                print(num_date, number_start, number_end)
                if num_date >= number_start:
                    if num_date <= number_end:
                        app.send_message(self.id,f'id={i[0]}, login={i[1]}, Имя={i[2]},Дата={i[3]},Начало={i[4]},Конец={i[5]},Общее время={i[6]}')
        except BaseException as e:
            print(e)
            app.send_message(self.id, "Ошибка вернись /start")





#Класс сотрудник
#Добавление времени начало
#Добавление времени конец
@app.message_handler(commands=['fellow_worker'])
def Fellow_worker(message):
    global wr
    wr = Fellow_worker(message.chat.username, message.chat.id)


@app.message_handler(commands=['time_start'])
def time_start(message):
    app.send_message(message.chat.id, f"ща все будет START")
    x = message.date
    wr.time_start(x)

@app.message_handler(commands=['time_end'])
def time_end(message):
    app.send_message(message.chat.id, f"ща все будет END ")
    wr.time_end()


#Добавление времени, главный критерий дата,
#добавление даты, ее проверка с настоящим временим<2 строка
#после добавления time_end берем данные статические создаем новую строку, в этой строке новая дата(на день вперед, читай 2 строка, для того чтобы нельзя
#было менять время) пустое значение time_start, time_end, переносится значение total_time(уже посчитанное) и пустой комментарий
#складываем total_time после внесения time_end/готово
#Отдельно функция которая достает имя и id сотрудника
#Прочтение коментария. Появляется
class Fellow_worker(New):
    def __init__(self, name, id):
        super().__init__(name,id)
        self.wor = tg.wor
        self.u_bd = tg.u_bd
        self.connection = tg.connection
        self.ruk = tg.ruk
        self.table_name = tg.table_name
        print(self.id, self.wor, self.ruk, self.name)
        self.name_id()
        app.send_message(self.id, '''
        1.Начало рабочего времени --/time_start--
        
        2.Конец рабочего времени --/time_end--
        
        (Предупреждение! После нажатия 'конец рабочего дня', данные невозможно изменить)
        ''')
        #инициализирует id и имя из строки конкретного пользователб в случае чего обратно добавить self.name_id
#start проверяет дату и если совпадает работает
    def time_start(self,date):
        #проверка, значение в таблице Null или нет
        #создаем новую строку после проверки
        #если None добавляем время в новую дату
        #Добавляем значение time_start только в строку с соотвествующей датой
        if self.check_line(date) == 1:
            self.new_line_user(date)
            data = self.time_teleg_now(date)#тк новая строка с обновленной датой созданна, вносим время в сегодняшнюю дату
            x = time.time()
            t = time.localtime(x)
            hour = str(t.tm_hour)
            min = str(t.tm_min)
            h_m_time = hour + ':' + min
            print(h_m_time)
            print(h_m_time.split(':'))
            try:
                req = f"UPDATE {self.table_name} SET time_start = '{h_m_time}' WHERE login_telegram = '{self.name}' AND data = '{str(data)}'"
                con = self.connection.cursor()
                con.execute(req)
                self.connection.commit()
            except Error as e:
                print(e)
        # создает чистую строку с новой датой
    def new_line_user(self, date):
        try:
            date = self.time_teleg_now(date)
            print(date, 'дата в строку')
            request = f"INSERT INTO {self.table_name}(login_telegram,name, data) VALUES ('{self.name}', '{self.table_username}', '{date}');"
            con = self.connection.cursor()
            con.execute(request)
            self.connection.commit()
            print('созданна новая строка')
        except Error as e:
            print(e)
#находим самое большое значение(дату) и после сравнение возращаем 1 или 0. 1 если даты разные, создаем новую строку
    def check_line(self, date):
        try:
            a = self.time_teleg_now(date)
            print(a, 'a')
            now_date = a.split('/')
            print(now_date, 'now_dATE')
            total_now_date = 0
            for i in now_date:
                total_now_date += int(i)
            print(total_now_date, 'total_now_date')
            n = self.name_id()
            max_total = n[5]
            print(max_total, total_now_date)
            if total_now_date != max_total:
                return 1
            else:
                return 0

        except BaseException as e:
                print(e)
                app.send_message(self.id, "Ошибка вернись")
        #время окончания добавляеться в строку с конкретной датой
    def time_end(self):
        x = time.time()
        t = time.localtime(x)
        hour = str(t.tm_hour)
        min = str(t.tm_min)
        h_m_time = hour + ':' + min
        try:
            req = f"UPDATE {self.table_name} SET time_end = '{h_m_time}' WHERE login_telegram = '{self.name}' AND data = '{self.data}'"
            con = self.connection.cursor()
            con.execute(req)
            self.connection.commit()
        except Error as e:
            print(e)
        self.time_total()
    #достать 2 значение(начало, конец) сложить, добавить в time_total
    def time_total(self):
        try:
            req = f"SELECT `time_start`,`time_end` FROM {self.table_name} WHERE `login_telegram` = '{self.name}' AND data = '{self.data}';"
            con = self.connection.cursor()
            con.execute(req)
            t = con.fetchall()
            print(t, type(t))
            t1 = t[0][0]
            t2 = t[0][1]
            print(t1, type(t1), t2, type(t2))

            h_m1 = t1.split(':')
            h_m2 = t2.split(':')

            h1 = int(h_m1[0])
            m1 = int(h_m1[1])
            h2 = int(h_m2[0])
            m2 = int(h_m2[1])

            h1 = h1*60
            h2 = h2*60
            total1 = h1+m1
            total2 = h2+m2
            total = total2 - total1
            h_total = total//60
            m_total = total%60
            print(h_total, ':', m_total)
            print()
        except Error as e:
            print(e)

        p_t = self.name_id()
        print(p_t, 'p_t')
        past_total3 = p_t[6]
        past_total2 = past_total3[-2][-2]
        if past_total2 == None:
            h_m_time = str(h_total) + ':' + str(m_total)
        else:
            past_total = past_total2.split(':')
            p_h = int(past_total[0])
            p_m = int(past_total[1])
            total_total_h = p_h + h_total
            total_total_m = p_m + m_total
            if total_total_m > 60:
                h1 = total_total_m//60
                total_total_h += h1
            h_m_time = str(total_total_h) + ':' + str(total_total_m)
        try:                                                                                                         #Error 001 сли не инициализировать time_start ошибка тк self.data None
            req = f"UPDATE {self.table_name} SET time_total = '{h_m_time}' WHERE login_telegram = '{self.name}' AND data = '{self.data}'"
            con = self.connection.cursor()
            con.execute(req)
            self.connection.commit()
        except Error as e:
            print(e)

#берем из строки id  и имя, дату для дальнейшей работы
    #Вся нужная информация о сотруднике
    def name_id(self):
        try:
            request = f"SELECT * FROM {self.table_name} WHERE login_telegram = '{self.name}';"
            print(request)
            watch1 = self.connection.cursor()
            watch1.execute(request)
            t = watch1.fetchall()
        except BaseException as e:
            print(e)
            app.send_message(self.id, f"Ошибка вернись /start {e}")
        past_line = t #список строк
        i = t[0]
        self.table_username = i[2]
        self.table_user_id = i[0]

        s_total = []
        for c in t:
            print(c, 'i')
            qwe = c[3]
            print(qwe, 'date_req',type(qwe) )
            if qwe == None:
                max_total = 0
            else:
                date = qwe.split('/')
                total = 0
                for x in date:
                    total += int(x)
                    s_total.append(total)
                    max_total = max(s_total)

        app.send_message(self.id, f'id={i[0]},  name={i[2]}')
        self.table_username = i[2]
        self.table_user_id = i[0]
        # max_total = max(s_total)
            #3-data[0], 4-time_start[1], 5-time_end[2], 6-time_total[3], 7 -comment[4], 8-max_total
        return i[3], i[4], i[5], i[6], i[7], max_total, past_line
    #check_line будет каждый раз обновлять дату для других методов
    def time_teleg_now(self, x):
        data_tel = x
        data_tel = time.localtime(data_tel)
        data = f'{data_tel.tm_mday}/{data_tel.tm_mon}/{data_tel.tm_year}'#текущая дата из чата
        self.data = data#Error 001
        return data












app.polling(none_stop=True)
