import os
import os.path
import random
import time
import telebot
from telebot import types

import config
import exercise_relax
import exercise_gym

TOKEN = config.TOKEN #ТОКЕН ВАШЕГО БОТА
bot = telebot.TeleBot(TOKEN)
complete_exercise = False


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    print(message.chat.id)
    print(message.from_user.id)
    bot.send_message(message.from_user.id,"Хорошая работа !")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Гимнастика для глаз.",
                                          callback_data="1s"))
    markup.add(types.InlineKeyboardButton(text="Снятие усталости/сухости.",
                                          callback_data="2s"))
    markup.add(types.InlineKeyboardButton(text="Глаза после операции.",
                                          callback_data="3s"))
    markup.add(types.InlineKeyboardButton(text=("Онлайн обращение "
                                                "к специалисту."),
                                          url="https://health.yandex.ru/"))
    bot.send_message(message.chat.id, 'По какой причине вы обратились ко мне:',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def delen(call):
    if call.data == "1s":
        textcall = ("Данный комплекс собрал в себе ряд упражнений, которые "
                    "хорошо подойдут как утренняя гимнастика, так и зарядка "
                    "после появления усталости в глазах.")
        bot.send_message(call.message.chat.id, textcall)
        markup2 = types.ReplyKeyboardMarkup(True, False)
        markup2.add(types.KeyboardButton("Да"))
        markup2.add(types.KeyboardButton("Нет"))
        mess = bot.send_message(call.message.chat.id, text="Начнем ?",
                                reply_markup=markup2)
        bot.register_next_step_handler(mess, go1)
    elif call.data == "2s":
        textcall = ("Хочу сразу предупредить. Чтобы был эффект от моих "
                    "упражнений в полной мере - повторять комплекс упражнений"
                    " необходимо несколько раз на день.")
        bot.send_message(call.message.chat.id, textcall)
        markup1 = types.ReplyKeyboardMarkup(True, False)
        markup1.add(types.KeyboardButton("Да"))
        markup1.add(types.KeyboardButton("Нет"))
        mess = bot.send_message(call.message.chat.id, text="Начнем ?",
                                reply_markup=markup1)
        bot.register_next_step_handler(mess, go2)
    elif call.data == "3s":
        textcall = ("Предупреждение: \nПосле лазерной коррекции(или иного рода"
                    " операций) необходимо 4 недели  избегать тех упражнений, "
                    "в которых нужно активно моргать, жмуриться, надавливать "
                    "на глаза — это может быть небезопасно и не лучшим образом"
                    " скажется на глаза")
        bot.send_message(call.message.chat.id, textcall)
        textcall = ("Так же, следует отметить, упражнения необходимо выполнять"
                    " регулярно для восстановления глаз и зрения.")
        bot.send_message(call.message.chat.id, textcall)
        markup1 = types.ReplyKeyboardMarkup(True, False)
        markup1.add(types.KeyboardButton("Да"))
        markup1.add(types.KeyboardButton("Нет"))
        mess = bot.send_message(call.message.chat.id, text="Начнем ?",
                                reply_markup=markup1)
        bot.register_next_step_handler(mess, go3)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.chat.id, ('Взаимодействуйте с ботом исключительно'
                                       ' через кнопки.\n\nЕсли вы заблудились '
                                       '- напишите\n/start.'))


def photo(num, c_id, dirr):
    """Проверка: если фото к упр. существует - отправляет его вместе с упр..
    num - номер упражнения.
    c_id - Чат-Id.
    dirr - название папки, в которой расположены фотографии по соответств упр..
    """
    link = (rf"{dirr}\ph{str(num)}.png")
    if os.path.isfile(link):
        with open(link, "rb") as img:
            bot.send_photo(c_id, photo=img)


def keybd(num, chat_id):
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(types.KeyboardButton("Следующее упражнение"))
    markup.add(types.KeyboardButton("Не хочу продолжать"))
    mesg = bot.send_message(chat_id, text=exercise_relax.exercise[num],
                            reply_markup=markup)
    return mesg


def keybdm(num, chat_id):
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(types.KeyboardButton("Следующее упражнение"))
    markup.add(types.KeyboardButton("Не хочу продолжать"))
    mesg = bot.send_message(chat_id, text=exercise_gym.exercises[num],
                            reply_markup=markup)
    return mesg


def end(chat_id):
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(types.KeyboardButton("Вызвать меню."))
    text = ("\nЕсли вы действительно хотите помочь помочь своим"
            " глазам и нацелены поддерживать их здоровье - выполняйте"
            " пожалуйста упражнения до конца.")
    answer = bot.send_message(chat_id, text, reply_markup=markup)
    return answer


rnd = list(range(len(exercise_relax.exercise))) 
rndm = list(range(len(exercise_gym.exercises))) #Списки, где числа без повтора.
# Сделано для того, чтобы упражнения всегда были рандомные и не повторялись.
# Сколько упражнений в файле relax и gym - столько чисел в списках.


def go1(message):
    if message.text == "Да":
        random.shuffle(rnd)
        random.shuffle(rndm)
        bot.send_message(message.chat.id, "Начнем же !")
        bot.send_message(message.chat.id, "И вот твое первое упражнение: ")
        mesg = keybdm(rndm[0], message.chat.id)
        photo(rndm[0], message.chat.id, "photo_gym")
        bot.register_next_step_handler(mesg, go1_1)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go1_1(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Продолжаем!\nСледующее упражнение:")
        mesg = keybdm(rndm[1], message.chat.id)
        photo(rndm[1], message.chat.id, "photo_gym")
        bot.register_next_step_handler(mesg, go1_2)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go1_2(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybdm(rndm[2], message.chat.id)
        photo(rndm[2], message.chat.id, "photo_gym")
        bot.register_next_step_handler(mesg, go1_3)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go1_3(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybd(rnd[3], message.chat.id)
        photo(rnd[3], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go1_4)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go1_4(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybd(rnd[4], message.chat.id)
        photo(rnd[4], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go1_5)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go1_5(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybdm(rndm[5], message.chat.id)
        photo(rndm[5], message.chat.id, "photo_gym")
        bot.register_next_step_handler(mesg, go1_6)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go1_6(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybdm(rndm[6], message.chat.id)
        photo(rndm[6], message.chat.id, "photo_gym")
        bot.register_next_step_handler(mesg, go1_7)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go1_7(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "И последнее упражнение: ")
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.add(types.KeyboardButton("Закончить комплекс упражнений."))
        mesg = bot.send_message(message.chat.id,
                                text=exercise_relax.exercise[rnd[7]],
                                reply_markup=markup)
        photo(rnd[7], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go1_8)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go1_8(message):
    text = ("Вы хорошо справились ! \nСоблюдая и выполняя регулярно комплекс "
            "этих упражнений вы защитите свои глаза от "
            "болезней и лишних проблем.")
    bot.send_message(message.chat.id, text)
    text = ("Так же, прошу заметить, если у вас появились проблемы со зрением "
            "и вы еще не обращались к соответствующим"
            " специалистам - самое время сделать это.")
    bot.send_message(message.chat.id, text)
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(types.KeyboardButton("Вернуться в главное меню."))
    text = ("Вы можете обратиться за онлайн консультацией"
            " в моем главном меню.\nБудьте здоровы !")
    mesg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(mesg, start_message)

########################################################


def go2(message):
    if message.text == "Да":
        random.shuffle(rnd)
        bot.send_message(message.chat.id, "Начнем же !")
        bot.send_message(message.chat.id, "И вот твое первое упражнение: ")
        mesg = keybd(rnd[0], message.chat.id)
        photo(rnd[0], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go2_1)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go2_1(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, ("Продолжаем !"
                                           "\nСледующее упражнение:"))
        mesg = keybd(rnd[1], message.chat.id)
        photo(rnd[1], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go2_2)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go2_2(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybd(rnd[2], message.chat.id)
        photo(rnd[2], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go2_3)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go2_3(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybd(rnd[3], message.chat.id)
        photo(rnd[3], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go2_4)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go2_4(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybd(rnd[4], message.chat.id)
        photo(rnd[4], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go2_5)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go2_5(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybd(rnd[5], message.chat.id)
        photo(rnd[5], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go2_6)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go2_6(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "Следующее упражнение: ")
        mesg = keybd(rnd[6], message.chat.id)
        photo(rnd[6], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go2_7)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go2_7(message):
    if message.text == "Следующее упражнение":
        bot.send_message(message.chat.id, "И последнее упражнение: ")
        markup = types.ReplyKeyboardMarkup(True, False)
        markup.add(types.KeyboardButton("Закончить комплекс упражнений."))
        mesg = bot.send_message(message.chat.id,
                                text=exercise_relax.exercise[rnd[7]],
                                reply_markup=markup)
        photo(rnd[7], message.chat.id, "photo_relax")
        bot.register_next_step_handler(mesg, go2_8)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go2_8(message):
    text = ("Вы хорошо справились !\nСоблюдая ежедневно комплекс упражнений и "
            "выполняя по 2-3 раза на сутки вы почувствуете"
            " большую разницу и изменения в вашем зрении.")
    bot.send_message(message.chat.id, text)
    text = ("Так же, прошу заметить, если у вас появились проблемы со зрением "
            "и вы еще не обращались к соответствующим специалистам "
            "- самое время сделать это.")
    bot.send_message(message.chat.id, text)
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(types.KeyboardButton("Вернуться в главное меню."))
    text = ("Вы можете обратиться за онлайн консультацией в"
            " моем главном меню.\nБудьте здоровы !")
    mesg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(mesg, start_message)
##############################################################################

#В данном блоке всегда будут одни и те же упражнения, т.к. в целом
# на глаза после операций мало упражнений, глаза больше должны отдахать.
def go3(message):
    if message.text == "Да":
        bot.send_message(message.chat.id, "Начнем")
        text = ("Первым упражнением у нас будет 'пальминг'.\nУпражнение "
                "выполняется следующим образом: необходимо занять удобную позу"
                " и закрыть глаза руками, таким образом, чтобы пальцы "
                "оказались на лбу, а ладони полностью накрыли глаза.")
        bot.send_message(message.chat.id, text)
        text = ("Следите, чтобы сквозь ладони не проникал свет – глаза должны"
                " оставаться в полной темноте. Ладони должны быть теплыми, так"
                " вы еще и прогреете глаза, что поспособствует большему "
                "расслаблению. Не давите на глазные яблоки, держите"
                " ладони слегка приподнятыми.")
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, ("Данное упражнение необходимо"
                                           " выполнять по 3-5 мин."))
        img = open(r"operac\oo1.png", "rb")
        bot.send_photo(message.chat.id, photo=img)
        answer = bot.send_message(message.chat.id, "Приступим через...")
        for i in range(20):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Приступим через..{str(20-i)} сек.")
            time.sleep(1)
        for i in range(10):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Выполнять осталось..{str(10-i)} сек.")
            time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=answer.message_id,
                              text="Упражнение можно закончить.")
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.add(types.KeyboardButton("Следуещее упражнение"))
        markup.add(types.KeyboardButton("Не хочу продолжать"))
        mesg = bot.send_message(message.chat.id, text="Умничка !",
                                reply_markup=markup)
        bot.register_next_step_handler(mesg, go3_1)
    else:
        answer = end(message.chat.id)
        bot.register_next_step_handler(answer, start_message)


def go3_1(message):
    if message.text == "Не хочу продолжать":
        answer = end(message.chat.id)
        bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(message.chat.id, "Второе упражнение:")
        text = ("Необходимо закрыть глаза, прикрыть ладонями и "
                "посидеть так 5 секунд. \n Далее убираем руки и как можно шире"
                " открываем глаза, все так же на 5 секунд."
                "\nУпражнение повторяем 3-4 раза.")
        bot.send_message(message.chat.id, text)
        img = open(r"operac\oo2.jpg", "rb") 
        bot.send_photo(message.chat.id, photo=img)
        answer = bot.send_message(message.chat.id, "Приступим через...")
        for i in range(15):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Приступим через..{str(15-i)} сек.")
            time.sleep(1)
        for i in range(30):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Выполнять осталось..{str(30-i)} сек.")
            time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=answer.message_id,
                              text="Упражнение можно закончить.")
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.add(types.KeyboardButton("Следуещее упражнение"))
        markup.add(types.KeyboardButton("Не хочу продолжать"))
        mesg = bot.send_message(message.chat.id, text="Замечательно",
                                reply_markup=markup)
        bot.register_next_step_handler(mesg, go3_2)


def go3_2(message):
    if message.text == "Не хочу продолжать":
        answer = end(message.chat.id)
        bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(message.chat.id, "Третье упражнение:")
        text = ("Смотрите поочерёдно сначала вверх, затем вниз, влево, вправо."
                " \nПовторяйте это упражнение до истечение таймера.")

        bot.send_message(message.chat.id, text)
        img = open(r"operac\oo3.png", "rb")
        bot.send_photo(message.chat.id, photo=img)
        answer = bot.send_message(message.chat.id, "Приступим через...")
        for i in range(20):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Приступим через..{str(20-i)} сек.")
            time.sleep(1)
        for i in range(25):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Выполнять осталось..{str(25-i)} сек.")
            time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=answer.message_id,
                              text="Упражнение можно закончить.")
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.add(types.KeyboardButton("Следуещее упражнение"))
        markup.add(types.KeyboardButton("Не хочу продолжать"))
        mesg = bot.send_message(message.chat.id, text="Молодец !",
                                reply_markup=markup)
        bot.register_next_step_handler(mesg, go3_3)


def go3_3(message):
    if message.text == "Не хочу продолжать":
        answer = end(message.chat.id)
        bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(message.chat.id, "Четвертое упражнение")
        text = ("Вращайте глазами по кругу сначало в одну сторону, затем в "
                "другую. \nПовторяйте это упражнение до истечения таймера.")
        bot.send_message(message.chat.id, text)
        text = ("Если будете чувствовать дискомфорт - закройте и расслабьте "
                "глаза, можете не выполнять данное упражнение до конца !")
        bot.send_message(message.chat.id, text)
        img = open(r"operac\oo4.png", "rb")
        bot.send_photo(message.chat.id, photo=img)
        answer = bot.send_message(message.chat.id, "Приступим через...")
        for i in range(10):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Приступим через..{str(10-i)} сек.")
            time.sleep(1)
        for i in range(40):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Выполнять осталось..{str(40-i)} сек.")
            time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=answer.message_id,
                              text="Упражнение можно закончить.")
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.add(types.KeyboardButton("Следуещее упражнение"))
        markup.add(types.KeyboardButton("Не хочу продолжать"))
        mesg = bot.send_message(message.chat.id, text="Отлично !",
                                reply_markup=markup)
        bot.register_next_step_handler(mesg, go3_4)


def go3_4(message):
    if message.text == "Не хочу продолжать":
        answer = end(message.chat.id)
        bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(message.chat.id, "Пятое упражнение: ")
        text = ("Сожмите веки, не морща лоб. Постарайтесь удерживать"
                " положение до 10 секунд.")
        bot.send_message(message.chat.id, text)
        text = ("В это время переводите взгляд от одного уголка глаза к "
                "другому (до 20 счетов).\nРасслабьте глаза на несколько сек..")
        bot.send_message(message.chat.id, text)
        text = ("Далее открываем глаза. Далее смотрим вверх-вниз, "
                "фокусируясь в каждой точке по 1-2 секунды.")
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, ("Повторяем это упражнение"
                                           " не больше 2-3 раз !"))
        img1 = open(r"operac\oo51.png", "rb")
        img2 = open(r"operac\oo52.png", "rb")
        img3 = open(r"operac\oo53.png", "rb")
        bot.send_photo(message.chat.id, photo=img1)
        bot.send_photo(message.chat.id, photo=img2)
        bot.send_photo(message.chat.id, photo=img3)
        answer = bot.send_message(message.chat.id, "Приступим через...")
        for i in range(10):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Приступим через..{str(10-i)} сек.")
            time.sleep(1)
        for i in range(40):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Выполнять осталось..{str(40-i)} сек.")
            time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=answer.message_id,
                              text="Упражнение можно закончить.")
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.add(types.KeyboardButton("Следуещее упражнение"))
        markup.add(types.KeyboardButton("Не хочу продолжать"))
        mesg = bot.send_message(message.chat.id, text="Супер !",
                                reply_markup=markup)
        bot.register_next_step_handler(mesg, go3_5)


def go3_5(message):
    if message.text == "Не хочу продолжать":
        answer = end(message.chat.id)
        bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(message.chat.id, "Последнее упражнение: ")
        bot.send_message(message.chat.id, ("Закройте глаза.\nРасслабьтесь."
                                           "\nПосидите в таком состоянии"
                                           "30-60 секунд."))
        answer = bot.send_message(message.chat.id, "Выполнять осталось...")
        for i in range(60):
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=answer.message_id,
                                  text=f"Выполнять осталось..{str(60-i)} сек.")
            time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=answer.message_id,
                              text="Упражнение можно закончить.")
        bot.send_message(message.chat.id,
                         "Вы молодец ! Комплекс упражнений успешно завершен.")
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.add(types.KeyboardButton("Вернуться в меню !"))
        text = ("Но необходимо отметить. Чтобы восстановление после операции "
                "шло значительно быстрее, данный комплекс необходимо выполнять"
                " 2-3 раза на день.")
        mesg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(mesg, start_message)
##########################################################################


bot.polling()
