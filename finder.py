import json
import os
import time
# Поиск по чатам
class ChatSearch:
    def __init__(self, log_file="chatLog.json", output_dir="search_results"):
        self.log_file = log_file
        self.output_dir = output_dir
        self.chat_log = self._load_log()

        # Создаем директорию для результатов, если ее нет
        os.makedirs(self.output_dir, exist_ok=True)
    # Считываем лог которая сохранила крутилка в файл chatLog.json
    def _load_log(self):
        # Проверяем, существует ли файл
        try:
            with open(self.log_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    # Функция для генерации уникального имени файла с временной меткой
    def _generate_filename(self, prefix):
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        return f"{self.output_dir}/{prefix}_{timestamp}.json"
    # Сохраняем результат поиска в файл JSON
    def _save_search_result(self, result, search_type, criteria):
        """Сохраняет результат поиска в файл JSON"""
        filename = self._generate_filename(f"{search_type}_{criteria}")

        result_data = {
            "search_type": search_type,
            "criteria": criteria,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "result_count": len(result),
            "results": result
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(result_data, file, ensure_ascii=False, indent=4)

        return filename
    # Поиск по участнику
    def _print_search_result(self, result, search_type, criteria):
        # Выводим результаты поиска в консоль
        print(f"\n{'='*50}")
        print(f"Результаты поиска: {search_type} = {criteria}")
        print(f"Найдено чатов: {len(result)}")
        print(f"{'='*50}")

        for i, chat in enumerate(result, 1):
            print(f"\nЧат #{i} (ID: {chat.get('Chat_id')}):")
            for j, event in enumerate(chat.get("events", []), 1):
                print(f"\nСобытие #{j}:")

                # Для сообщений
                if "message" in event:
                    print(f"  Тип: Сообщение")
                    print(f"  Участник: {event.get('name')}")
                    print(f"  Сообщение: {event.get('message')}")
                    print(f"  Дата: {event.get('date')} {event.get('time')}")

                # Для событий завершения
                elif event.get("action") == "Завершение чата":
                    print(f"  Тип: Завершение чата")
                    print(f"  Статус: {event.get('status')}")

                    if "mark" in event:
                        mark = event.get('mark', 'не указана')
                        print(f"  Оценка: {mark}")

                    print(f"  Пользователь: {event.get('user')}")
                    print(f"  Оператор: {event.get('operator')}")
            print("-"*50)
    # Тут выбираем тип поиска и критерий
    def search_and_save(self, search_type, criteria):
        """Выполняет поиск, сохраняет результат в JSON и выводит в консоль"""
        # Выбираем тип поиска
        if search_type == "participant":
            result = self.find_by_participant(criteria)
        elif search_type == "operator":
            result = self.find_by_operator(criteria)
        elif search_type == "user":
            result = self.find_by_user(criteria)
        elif search_type == "chat_id":
            result = [self.find_by_chat_id(criteria)] if self.find_by_chat_id(criteria) else []
        elif search_type == "mark":
            result = self.find_by_mark(criteria)
        elif search_type == "status":
            result = self.find_by_status(criteria)
        else:
            print("Неподдерживаемый тип поиска")
            return

        # Сохраняем результат
        filename = self._save_search_result(result, search_type, criteria)
        print(f"Результаты сохранены в файл: {filename}")

        # Выводим результат
        self._print_search_result(result, search_type, criteria)

        return result

    # Методы поиска по участникам, операторам, пользователям и чатам
    def find_by_participant(self, participant_id):
        result = []
        for chat in self.chat_log:
            for event in chat.get("events", []):
                if (event.get("name") == participant_id or
                        event.get("user") == participant_id or
                        event.get("operator") == participant_id):
                    result.append(chat)
                    break
        return result
    # Поиск по операторам
    def find_by_operator(self, operator_id):
        result = []
        for chat in self.chat_log:
            for event in chat.get("events", []):
                if (event.get("name") == operator_id or
                        event.get("operator") == operator_id):
                    result.append(chat)
                    break
        return result
    # Поиск по пользователям
    def find_by_user(self, user_id):
        result = []
        for chat in self.chat_log:
            for event in chat.get("events", []):
                if (event.get("name") == user_id or
                        event.get("user") == user_id):
                    result.append(chat)
                    break
        return result
    # Поиск по ID чата
    def find_by_chat_id(self, chat_id):
        for chat in self.chat_log:
            if chat.get("Chat_id") == chat_id:
                return chat
        return None
    # Поиск по оценке
    def find_by_mark(self, mark_value):
        result = []
        for chat in self.chat_log:
            for event in chat.get("events", []):
                if event.get("action") == "Завершение чата" and event.get("mark") == mark_value:
                    result.append(chat)
                    break
        return result
    # Поиск по статусу
    def find_by_status(self, status):
        result = []
        for chat in self.chat_log:
            for event in chat.get("events", []):
                if event.get("action") == "Завершение чата" and event.get("status") == status:
                    result.append(chat)
                    break
        return result
    # Получаем все чаты из лога
    def get_all_chats(self):
        print(f"Всего чатов: {len(self.chat_log)}")
        return self.chat_log