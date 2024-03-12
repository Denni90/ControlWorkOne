import json
import os
from datetime import datetime


def add_note():
    notes = load_note()
    new_note = [len(notes) + 1,
                input("Введите заголовок заметки: "),
                input("Введите текст заметки: "),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    notes.append(new_note)
    save_note(notes)
    print("Заметка успешно создана!")


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, tuple):
            return list(obj)
        elif isinstance(obj, dict):
            return {self.default(k): self.default(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.default(item) for item in obj]
        return obj


def save_note(notes):
    with open('notes.json', 'w') as file:
        json.dump(notes, file, cls=CustomEncoder)


def load_note():
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as file:
            notes = json.load(file)
        return notes
    else:
        return []


def edit_note(note_id):
    notes = load_note()
    for note in notes:
        if note[0] == note_id:
            note[1] = input("Введите новый заголовок заметки: ")
            note[2] = input("Введите новый текст заметки: ")
            note[3] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_note(notes)
            print("Заметка успешно отредактирована.")
            return
    print("Заметка с таким id не найдена.")


def delete_note(note_id):
    notes = load_note()
    filtered_notes = [note for note in notes if note[0] != note_id]

    if len(filtered_notes) == len(notes):
        print("Заметка с таким id не найдена.")
    else:
        save_note(filtered_notes)
        print("Заметка успешно удалена.")


def list_notes(since=None):
    notes = load_note()
    if since:
        notes = [note for note in notes if note[0] >= since]
    for note in notes:
        print(note)


while True:
    print("\nМеню:")
    print("1. Создать")
    print("2. Показать список")
    print("3. Редактировать")
    print("4. Удалить")
    print("5. Выйти")

    choice = input("Выбрать действие: ")

    if choice == "1":
        add_note()
    elif choice == "2":
        list_notes()
    elif choice == "3":
        note_id = int(input("Введите id заметки для редактирования: "))
        edit_note(note_id)
    elif choice == "4":
        note_id = int(input("Введите id заметки для удаления: "))
        delete_note(note_id)
    elif choice == "5":
        break
    else:
        print("Неверный выбор. Пожалуйста, попробуйте снова.")
