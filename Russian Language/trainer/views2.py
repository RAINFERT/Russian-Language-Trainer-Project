from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse
import random
import csv

def index(request):
    """Главная страница для примеров использования слов"""
    examples = get_examples_from_csv()
    return render(request, "index.html", context={"examples": examples})

def add_example(request):
    return render(request, "example_add.html")

def examples_list(request):
    """Отображение списка примеров"""
    examples = get_examples_from_csv()
    return render(request, "example_list.html", context={"examples": examples})

def send_example(request):
    """Обработка отправки примера"""
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name") or "user"  # по умолчанию "user"
        word = request.POST.get("word", "")
        example_sentence = request.POST.get("example_sentence", "").replace(";", ",")
        translation = request.POST.get("translation", "").replace(";", ",")
        context = {"user": user_name}

        if len(example_sentence) == 0:
            context["success"] = False
            context["comment"] = "The example must not be empty"
        elif len(word) == 0:
            context["success"] = False
            context["comment"] = "The word must be specified"
        elif len(translation) == 0:
            context["success"] = False
            context["comment"] = "Translation must not be empty"
        else:
            if write_example_to_csv(word, example_sentence, user_name):
                context["success"] = True
                context["comment"] = "Your example is accepted"
            else:
                context["success"] = False
                context["comment"] = "Such an example already exists or an error occurred"

        return render(request, "example_request.html", context)
    else:
        return add_example(request)

def get_examples_from_csv():
    """Чтение примеров из CSV файла"""
    examples = []
    try:
        with open("./data/examples.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                if len(row) == 4:
                    word, example_sentence, translation, author = row
                elif len(row) == 3:
                    word, example_sentence, author = row
                    translation = ""
                elif len(row) == 2:
                    word, example_sentence = row
                    translation = ""
                    author = "db"  # для старых записей
                else:
                    continue
                examples.append({
                    "word": word.strip(),
                    "example_sentence": example_sentence.strip(),
                    "translation": translation.strip(),
                    "author": author.strip()
                })
    except FileNotFoundError:
        pass
    return examples

def write_example_to_csv(word, example_sentence, translation, author):
    """Запись нового примера в CSV файл"""
    try:
        # Проверка на дубликаты
        existing = get_examples_from_csv()
        for ex in existing:
            if ex["word"].lower() == word.lower() and ex["example_sentence"].strip().lower() == example_sentence.strip().lower():
                return False  # уже существует

        with open("./data/examples.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([word, example_sentence, translation, author])
        return True
    except Exception:
        return False