import random
from django.shortcuts import render, redirect
from django.core.cache import cache
from . import words_w



def index(request):
    return render(request, "index.html")

def words_list(request):
    words = words_w.get_words_for_table()
    return render(request, "word_list.html", context={"words": words})

def add_word(request):
    return render(request, "word_add.html")

def send_word(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_word = request.POST.get("new_word", "")
        new_translation = request.POST.get("new_translation", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_translation) == 0:
            context["success"] = False
            context["comment"] = "Translation must not be empty"
        elif len(new_word) == 0:
            context["success"] = False
            context["comment"] = "The word must not be empty"
        else:
            if words_w.write_word(new_word, new_translation):
                context["success"] = True
                context["comment"] = "Your word is accepted"
            else:
                context["success"] = False
                context["comment"] = "The word already exists"

        return render(request, "word_request.html", context)

    return add_word(request)

def test_words(request):
    words = words_w.get_words_for_table()
    if not words:
        return render(request, "test_words.html", {"error": "Нет слов для теста"})


    if request.method == "POST":
        # Достаём правильный ответ из сессии
        word = request.session.get("test_word", "")
        translation = request.session.get("test_translation", "")
        user_answer = request.POST.get("answer", "").strip()
        total_attempts = request.session.get('total_attempts', 0) + 1
        request.session['total_attempts'] = total_attempts

        # Проверка правильности
        if user_answer.lower() == translation.lower():
            # Увеличим счетчик правильных ответов
            correct_user_answers = request.session.get('correct_user_answers', 0) + 1
            request.session['correct_user_answers'] = correct_user_answers

            context = {
                "result": "success",
                "message": "Correct answer!",
                "word": word,
                "translation": translation
            }
        else:
            context = {
                "result": "failure",
                "message": f"Incorrect! Correct answer: {translation}",
                "word": word,
                "translation": translation
            }

        # Выбираем следующее слово и сохраняем в сессию
        next_word_data = random.choice(words)
        request.session["test_word"] = next_word_data[1]
        request.session["test_translation"] = next_word_data[2]
        context["next_word"] = next_word_data[1]

        return render(request, "test_words.html", context)

    else:  # GET-запрос — показать новое слово
        random_word = random.choice(words)
        word, translation = random_word[1], random_word[2]
        request.session["test_word"] = word
        request.session["test_translation"] = translation
        return render(request, "test_words.html", {"word": word})

# views.py
def reset_test(request):
    request.session['correct_user_answers'] = 0
    request.session['total_attempts'] = 0
    request.session['total_words'] = 0
    return redirect("test_words")  # перенаправление на тест



def show_stats(request):
    # Получаем количество правильно угаданных слов из сессии
    correct_user_answers = request.session.get('correct_user_answers', 0)
    total_attempts = request.session.get('total_attempts', 0)
    stats = words_w.get_words_stats(correct_user_answers)
    stats["correct_user_answers"] = correct_user_answers
    stats["total_attempts"] = total_attempts
    return render(request, "stats.html", stats)