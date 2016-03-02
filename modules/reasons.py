import random

import modules

filename = 'chapter'
chapter = None


def get_words(submission_type):
    global chapter
    # Load the file if it has not been loaded - first load
    if chapter is None:
        version, data = modules.get_readable(filename)
        # If the file is able to be loaded
        if data:
            chapter = data
        else:
            chapter = {'title': [], 'passage': []}
    # Get the desired word list
    if submission_type in ('title', 'passage'):
        return chapter[submission_type]
    else:
        return None


def save_words():
    global chapter
    modules.save_readable(chapter, filename, version=1)


@modules.register(rule=[r"$@bot", r"what would Roger do\?"])
def advise_roger_action(bot, msg):
    """
    Create the title of a chapter in Roger's Reasons.
    """
    titles = get_words('title')

    if titles:
        title = random.choice(titles)
        title.capitalize()
        bot.reply("Chapter {number}: {title}".format(
            number=random.randint(1, 60),
            title=title,
        ))
    else:
        bot.reply("Don't ask questions you don't want the answer to.")


@modules.register(rule=[r"$@bot", r"what does Roger think\?"])
def bestow_roger_wisdom(bot, msg):
    """
    Provide a passage from one of the chapters of Roger's Reasons.
    """
    passages = get_words('passage')

    if passages:
        text = random.choice(passages)
        # Make sure first word is capitalized or so help me...
        text[0].upper()
        bot.reply("{text}".format(
            text=text,
        ))
    else:
        bot.reply("That's one secret he'll never tell.")


@modules.register(rule=[r"$@bot", r"add", r"(title|passage)", r"([\w ,-]+)$"])
def add_to_book(bot, msg, word_type, word):
    """
    Add chapter titles and passages.
    """
    word = word.strip()

    book_portion = get_words(word_type)
    if book_portion is None:
        bot.reply("Maybe try adding an insult, dingus.")
        return
    if word in book_portion:
        bot.reply("I see you're well-versed in the timeless classic, \"Roger\'s Reasons.\"")
        return
    if not word:
        bot.reply("NOT UP IN HERE.")
        return

    book_portion.append(word)
    save_words()
    bot.reply("Added.")
