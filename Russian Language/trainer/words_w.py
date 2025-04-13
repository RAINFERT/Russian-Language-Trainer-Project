def get_words_for_table():
    words = []
    with open("./data/words.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:
            word, translation, source = line.split(";")
            words.append([cnt, word, translation])
            cnt += 1
    return words


def write_word(new_word, new_translation):
    new_word_line = f"{new_word};{new_translation};user"
    with open("./data/words.csv", "r", encoding="utf-8") as f:
        existing_words = [l.strip("\n") for l in f.readlines()]
        title = existing_words[0]
        old_words = existing_words[1:]

    # Проверка, существует ли уже это слово
    for line in old_words:
        word, translation, _ = line.split(";")
        if word.strip().lower() == new_word.strip().lower():
            return False

    words_sorted = old_words + [new_word_line]
    words_sorted.sort()
    new_words = [title] + words_sorted
    with open("./data/words.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_words))

    return True


def get_words_stats(correct_user_answers=0):
    db_words = 0
    user_words = 0
    with open("./data/words.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            word, trans, added_by = line.split(";")

            if "user" in added_by:
                user_words += 1
            elif "db" in added_by:
                db_words += 1
    stats = {
        "words_all": db_words + user_words,
        "words_own": db_words,
        "words_added": user_words,
        "correct_user_answers": correct_user_answers
    }
    return stats