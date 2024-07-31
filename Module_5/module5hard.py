'''
Дополнительное практическое задание по модулю*
Дополнительное практическое задание по модулю: "Классы и объекты."

Цель: Применить знания полученные в модуле, решив задачу повышенного уровня сложности.

Задание "Свой YouTube":
Университет Urban подумывает о создании своей платформы, где будут размещаться дополнительные полезные ролики
на тему IT (юмористические, интервью и т.д.). Конечно же для старта написания интернет ресурса требуются хотя бы
базовые знания программирования.

Именно вам выпала возможность продемонстрировать их, написав небольшой набор классов, которые будут выполнять
похожий функционал на сайте.

Всего будет 3 класса: UrTube, Video, User.

Общее ТЗ:
Реализовать классы для взаимодействия с платформой, каждый из которых будет содержать методы добавления видео,
авторизации и регистрации пользователя и т.д.

Подробное ТЗ:

Каждый объект класса User должен обладать следующими атрибутами и методами:
Атриубуты: nickname(имя пользователя, строка),
password(в хэшированном виде { https://pythonim.ru/osnovy/funktsiya-hash-v-python }, число), age(возраст, число)
Каждый объект класса Video должен обладать следующими атрибутами и методами:
Атриубуты: title(заголовок, строка), duration(продолжительность, секунды), time_now(секунда остановки (изначально 0)),
adult_mode(ограничение по возрасту, bool (False по умолчанию))
Каждый объект класса UrTube должен обладать следующими атрибутами и методами:
 Атриубты: users(список объектов User), videos(список объектов Video), current_user(текущий пользователь, User)
Метод log_in, который принимает на вход аргументы: nickname, password и пытается найти пользователя в users с такими
же логином и паролем. Если такой пользователь существует, то current_user меняется на найденного. Помните,
что password передаётся в виде строки, а сравнивается по хэшу.
Метод register, который принимает три аргумента: nickname, password, age, и добавляет пользователя в список, если
пользователя не существует (с таким же nickname). Если существует, выводит на экран: "Пользователь {nickname} уже
существует". После регистрации, вход выполняется автоматически.
Метод log_out для сброса текущего пользователя на None.
Метод add, который принимает неограниченное кол-во объектов класса Video и все добавляет в videos, если с таким же
названием видео ещё не существует. В противном случае ничего не происходит.
Метод get_videos, который принимает поисковое слово и возвращает список названий всех видео, содержащих поисковое слово.
Следует учесть, что слово 'UrbaN' присутствует в строке 'Urban the best' (не учитывать регистр).
Метод watch_video, который принимает название фильма, если не находит точного совпадения(вплоть до пробела), то ничего
не воспроизводится, если же находит - ведётся отчёт в консоль на какой секунде ведётся просмотр. После текущее время
просмотра данного видео сбрасывается.
Для метода watch_video так же учитывайте следующие особенности:
Для паузы между выводами секунд воспроизведения можно использовать функцию sleep из
модуля time { https://pythonim.ru/osnovy/funktsiya-hash-v-python }.
Воспроизводить видео можно только тогда, когда пользователь вошёл в UrTube. В противном случае выводить в консоль
надпись: "Войдите в аккаунт, чтобы смотреть видео"
Если видео найдено, следует учесть, что пользователю может быть отказано в просмотре, т.к. есть ограничения 18+.
Должно выводиться сообщение: "Вам нет 18 лет, пожалуйста покиньте страницу"
После воспроизведения нужно выводить: "Конец видео"

Код для проверки:
ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')

Вывод в консоль:
['Лучший язык программирования 2024 года']
['Лучший язык программирования 2024 года', 'Для чего девушкам парень программист?']
Войдите в аккаунт, чтобы смотреть видео
Вам нет 18 лет, пожалуйста покиньте страницу
1 2 3 4 5 6 7 8 9 10 Конец видео
Пользователь vasya_pupkin уже существует
urban_pythonist

Примечания:
Не забывайте для удобства использовать dunder(магические) методы:
__str__, __repr__, __contains__, __eq__ и др.
(повторить можно здесь { https://docs.python.org/3/reference/datamodel.html#basic-customization })
Чтобы не запутаться рекомендуется после реализации каждого метода проверять как он работает,
тестировать разные вариации.
___________________________________________________________________
'''

import time
import hashlib


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self.hash_password(password)  # Хэшируем пароль
        self.age = age

    def hash_password(self, password):
        '''
        Хэширование пароля.
        Преобразовываем строку в байты с помощью encode()
        И для того, что бы получить хеш в виде шестнадцатеричной строки, использую метод hexdigest()
        Выбор пал на md5, так как в нашей задаче, принципиальной разницы нету в алгоритме метода шифрования.
        А вообще он меньше (128b) чем sha-256 и короче в написании. :)
        '''
        return hashlib.md5(password.encode()).hexdigest()

    def __str__(self):
        return f'Пользователь: {self.nickname}'

    def __repr__(self):
        return f'Пользователь ("{self.nickname}", "{self.password}", {self.age})'


class Video:
    def __init__(self, title, duration, time_now=0, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode

    def __str__(self):
        return f'Видео: {self.title} ({self.duration} сек.)'

    def __repr__(self):
        return f'Видео("{self.title}", {self.duration}, {self.time_now}, {self.adult_mode})'


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        '''
        Авторизация пользователя.
        '''
        for user in self.users:
            if user.nickname == nickname and user.password == self.hash_password(password):
                self.current_user = user
                print(f'Вход выполнен как {user.nickname}')
                return True
        print('Неверный логин и пароль')
        return False

    def register(self, nickname, password, age):
        '''
        Регистраци янового пользователя.
        '''
        for user in self.users:
            if user.nickname == nickname:
                print(f'Пользователь {nickname} уже существует')
                return False

        new_user = User(nickname, password, age)
        self.users.append(new_user)
        print(f'Регистрация завершена. Вы вошли как {nickname}')
        self.current_user = new_user
        return True

    def log_out(self):
        '''
        Выход и аккаунта.
        '''
        self.current_user = None
        print('Вы вышли из аккаунта')

    def add(self, *videos):
        '''
        Добавление видео на платформу.
        '''
        for video in videos:
            if video not in self.videos:
                self.videos.append(video)
                print(f'Видео {video.title} добавлено.')

    def get_videos(self, search_term):
        '''
        Поиск видео по ключевому слову.
        '''
        search_term = search_term.lower()
        found_videos = []
        for video in self.videos:
            if search_term in video.title.lower():
                found_videos.append(video.title)
        return found_videos

    def watch_video(self, title):
        '''
        Просмотр видео.
        '''
        if not self.current_user:
            print('Войдите в аккаунт, что бы смотреть видео')
            return

        found_video = None
        for video in self.videos:
            if video.title == title:
                found_video = video
                break

        if not found_video:
            print('Видео не найдено')
            return

        if found_video.adult_mode and self.current_user.age < 18:
            print('Вам нет 18 лет, пожалуйста покиньте страницу')
            return

        print(f'Просмотр видео: {found_video.title}')
        for i in range(found_video.time_now + 1, found_video.duration + 1):
            print(f'Секунда: {i}')
            time.sleep(1)
            found_video.time_now = 1
        print('Конец видео')


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
