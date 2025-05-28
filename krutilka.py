import random
import json
import time
import finder # Импотриуем наш модуль на для поиска



# Создаем класс юзера
class User:
    def __init__(self, name, date, city):
        self.__name = name
        self.__date = date
        self.__city = city
        self.__settedMark = None
    # Делаем геттер для имени
    def getName(self):
        return self.__name
    # функция для создания чата
    def makeChat(self, operator, chat_id):
        chat = Chat(chat_id, operator, self)
        chat.addMessage(self, self.sendMessage())
        operator.sendAnswer(chat)
        return chat
    # Функция для установки оценки
    def setMark(self, operator, chat):
        chat_status = operator.closeChat(chat)
        if chat_status == 1:  # Чат успешно завершен
            markList = [None, 1, 2, 3, 4, 5]    # Список возможных оценок
            self.__settedMark = random.choice(markList)

            # Всегда логируем успешное завершение с mark (даже если None)
            chat.logCompletion(
                status="успешно завершен",
                user=self,
                operator=operator,
                mark=self.__settedMark
            )
        else:  # Чат не завершен
            chat.logCompletion(
                status="чат не завершен",
                user=self,
                operator=operator
            )
    # Функция для отправки сообщения
    def sendMessage(self):
        return random.randint(0, 100)

# Создаем класс оператора
class Operator:
    def __init__(self, name, login, date, city, position, experience):
        self.__name = name
        self.__login = login
        self.__date = date
        self.__city = city
        self.__position = position
        self.__experience = experience
    # Делаем геттер для имени
    def getName(self):
        return self.__name
    # Функция для отправки сообщения
    def sendAnswer(self, chat):
        message = random.randint(0, 100)
        chat.addMessage(self, message)
        return message
    # Функция для закрытия чата
    def closeChat(self, chat):
        return random.randint(0, 1)

# Создаем класс чата
class Chat:
    def __init__(self, id, operator, user):
        self.__id = id
        self.__operator = operator
        self.__user = user
    # Делаем геттер для id
    def getId(self):
        return self.__id
    # Функция для добавления сообщения
    def addMessage(self, sender, message):
        chatText = {
            "Chat_id": self.getId(),
            "name": sender.getName(),
            "message": message,
            "date": time.strftime("%x"),
            "time": time.strftime("%X")
        }
        chatLog(self.__id, chatText)
        return chatText
    # Функция для логирования завершения чата
    def logCompletion(self, status, user, operator, mark=None):
        completion_event = {
            "action": "Завершение чата",
            "status": status,
            "user": user.getName(),
            "operator": operator.getName()
        }

        # Для завершенных чатов всегда добавляем mark
        if status == "успешно завершен":
            completion_event["mark"] = mark  # Может быть числом или None

        chatLog(self.__id, completion_event)
# Функция для логирования событий
def chatLog(chat_id, event):
    # Читаем существующие данные или создаем пустой список
    try:
        with open("chatLog.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Ищем чат с нужным ID
    chat_found = False
    for chat in data:
        if chat["Chat_id"] == chat_id:
            chat["events"].append(event)
            chat_found = True
            break

    # Если чат не найден - создаем новый
    if not chat_found:
        data.append({
            "Chat_id": chat_id,
            "events": [event]
        })

    # Записываем обновленные данные
    with open("chatLog.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Генерируем данные для операторов
def generateOperator():
    operatorList = []
    for _ in range(100):
        operator = {
            "name": random.randint(0, 1000),
            "login": random.randint(0, 1000),
            "date": random.randint(0, 1000),
            "city": random.randint(0, 1000),
            "position": random.randint(0, 100),
            "experience": random.randint(0, 100)
        }
        operatorList.append(operator)

    with open("Operators.json", "w", encoding="utf-8") as file:
        json.dump(operatorList, file, ensure_ascii=False, indent=4)

    return operatorList

# Генерируем данные для юзеров
def generateUser():
    userList = []
    for _ in range(100):
        user = {
            "name": random.randint(0, 1000),
            "date": random.randint(0, 1000),
            "city": random.randint(0, 1000)
        }
        userList.append(user)

    with open("Users.json", "w", encoding="utf-8") as file:
        json.dump(userList, file, ensure_ascii=False, indent=4)

    return userList

# Запускаем симуляцию для 100 чатов
def simulation():
    userList = generateUser() # Заполняем список юзеров сгенерированными данными
    operatorList = generateOperator() # Заполняем список операторов сгенерированными данными
    # создаем экземпляры юзеров и операторов
    users = [User(name=data["name"], date=data["date"], city=data["city"]) for data in userList]
    operators = [Operator(
        name=data["name"],
        login=data["login"],
        date=data["date"],
        city=data["city"],
        position=data["position"],
        experience=data["experience"]
    ) for data in operatorList]
    # Создаем 100 чатов и двигаемся по списку юзеров
    for i in range(len(users)):
        user = users[i]
        if operators:
            selectedOperator = random.choice(operators) # Выбираем случайного оператора который будет отвечать на чат
            chat = user.makeChat(selectedOperator, i)   # Создаем чат
            user.setMark(selectedOperator, chat) # Устанавливаем оценку
            operators.remove(selectedOperator) # Удаляем оператора из списка

# Запускаем симуляцию
if __name__ == "__main__":
    simulation()
    # Инициализируем наш модуль
    search = finder.ChatSearch()
    # Ищем чаты с 5 оценкой
    chats_with_5 = search.search_and_save("mark", 5)
    # Ищем чаты которые закрыты
    chats_by_status = search.search_and_save("status", "успешно завершен")
    # Ищем чаты с оператором 274 или любым другим оператором, список операторов в файле Operators.json
    chats_by_operator = search.search_and_save("operator", "274")
    # Ищем чат с id 1
    chats_by_id = search.search_and_save("id", 1)
    # Вывод всех чатов
    getAll = search.get_all_chats()
