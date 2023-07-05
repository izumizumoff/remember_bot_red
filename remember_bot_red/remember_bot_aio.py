import logging
import json
from aiogram.types import message
import asyncio
from aiogram import Bot, Dispatcher, types, executor
import config

# логирование процесса
logging.basicConfig(level=logging.INFO)

# создаем экземпляр и передаем ему token нашего бота
bot = Bot(
    token=config.BOT_TOKEN,
    parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)

admin_id = config.ADMIN_ID
zriteli_list = []
zritel_index = 0
voina_index = 1
start_set = set()


# функция иформирования о зрителях
async def users_info(id_func):
    with open('users.json', 'r') as users_file:
        all_users = json.load(users_file)
    users_list = list(all_users)
    users_list.sort()
    info = ''
    for x in range(len(users_list)):
        info = info + str(x+1) + '. ' + users_list[x] + ': '+ all_users[users_list[x]] + '\n'

    await bot.send_message(id_func, info)

# функция зацикленного переключения хода зрителя
def turn_index():
    global zritel_index
    if len(zriteli_list) > 1:
        if zritel_index == len(zriteli_list) - 1:
            zritel_index = 0
        else:
            zritel_index = zritel_index + 1
    else:
        pass

# установка администратора
@dp.message_handler(commands='admin')
async def send_welcome(message: types.Message):
    global admin_id
    admin_id = message.from_user.id

    keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_menu.add('PLAY')
    keyboard_menu.row('1. ТЕЛЕГРАММЫ')
    keyboard_menu.add('2. КОНЕЦ ТЕЛЕГРАММ')
    keyboard_menu.row('3. ТРОЛЛЕЙБУС')
    keyboard_menu.add('4. КОНЕЦ ТРОЛЛЕЙБУСА')
    keyboard_menu.row('5. КОМНАТА первая', '6. КОМНАТА вторая', '7. КОМНАТА третья')
    keyboard_menu.add('8. КОНЕЦ КОМНАТЫ')
    keyboard_menu.row('9. ВОЙНА', '10. СТИХ')
    keyboard_menu.add('11. КОНЕЦ ВОЙНЫ')
    keyboard_menu.row('12. СВОБОДА', '13. ФИНАЛ')
    keyboard_menu.add('#ЗАКРЫТЬ_МЕНЮ')
    await bot.send_message(
        message.from_user.id, 
        'Теперь ты админ', reply_markup=keyboard_menu)
    
@dp.message_handler(text='#ЗАКРЫТЬ_МЕНЮ')
async def send_welcome(message: types.Message):
    await bot.send_message(
        message.from_user.id, 
        'Меню закрыто. Чтоб открыть введи /admin', reply_markup=types.ReplyKeyboardRemove())

##!!! админская команда - всех зрителей стирает
@dp.message_handler(commands='reset')
async def reset(message: types.Message):
    global zriteli_list
    global zritel_index
    global start_set
    global admin_id
    global voina_index
    
    if message.from_user.id == admin_id:
        empty_dict = {}
        with open('users.json', 'w') as empty_file:
            json.dump(empty_dict, empty_file)
        zritel_index = 0
        zriteli_list = []
        start_set = set()
        voina_index = 1
        await bot.send_message(
            admin_id,
            'обнулилось все!'
        )
    else:
        pass
    

##!!! админская команда - сохраняет из файла в список зрителей
@dp.message_handler(commands='save')
async def save(message: types.Message):
    global zriteli_list
    global admin_id

    if message.from_user.id == admin_id:
        with open('users.json', 'r') as all_users:
            zriteli_list = list(json.load(all_users))
        await bot.send_message(
            admin_id,
            'Сохранил из файла в список участников'
        )
    else:
        pass

# при первом подключении /start
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    
    global start_set
    start_set.add(str(message.from_user.id))

    await bot.send_message(
        message.from_user.id,
        config.START_MESSAGE[0]
    )

    await asyncio.sleep(16)
    await types.ChatActions.typing()
    await asyncio.sleep(4)

    await bot.send_message(
        message.from_user.id,
        config.START_MESSAGE[1]
    )

# при ответе на "готов"
@dp.message_handler(lambda message: message.text and 'готов' in message.text.lower())
async def send_welcome(message: types.Message):
    global admin_id
    
    # открываем файл со словарем всех  пользователей
    with open('users.json', 'r') as file_new_users:
        new_users = json.load(file_new_users)
    # Добавляем в список  нового пользователя (id - ключ, имя и фамилия - значения)
    if str(message.from_user.id) in new_users:
        await bot.send_message(
            message.from_user.id,
            'Я понял, что готов!')
    else:
        if message.from_user.first_name and message.from_user.last_name:
            new_users[message.from_user.id] = message.from_user.first_name + ' ' + message.from_user.last_name
        else:
             new_users[message.from_user.id] = str(message.from_user.id)
        # сохраняем файл обратно в словарь
        with open('users.json', 'w') as file_save_users:
            json.dump(new_users, file_save_users, ensure_ascii = False)
        
        await bot.send_message(
            message.from_user.id,
            'Отлично, что ты с нами! Скоро спектакль начнется! Жди сообщения')
        
        await users_info(admin_id)


# запуск игры
# формирование списка зрителей
# отправка смс всем зрителям "проходите в первый зал (день первый)"
@dp.message_handler(text='PLAY')
async def send_play(message: types.Message):
    global zriteli_list
    global admin_id

    with open('users.json', 'r') as file:
        list_fo_play = json.load(file)
    
    if list_fo_play:
        await bot.send_message(
            admin_id,
            'Внимание! Спектакль начался!'
        )

        with open('users.json', 'r') as all_users:
            zriteli_list = list(json.load(all_users))
        await asyncio.sleep(1)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Проходите в первый зал (ДЕНЬ ПЕРВЫЙ). Спектакль начинается!')
        # ждем 30 сек пока идут в первый зал
        await asyncio.sleep(30)

        for x in zriteli_list:
            await bot.send_message(
                x,
                'Все дошли?\nГотовы?\n\nЕсли готовы то располагайтесь удобней!\n\n\n Часть первая:\n#оважном')
        await bot.send_message(admin_id, 'Запускай часть первую: ТЕЛЕГРАММЫ')
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')




## часть_1 с телеграммами (первый зал с трибуной)
@dp.message_handler(text='1. ТЕЛЕГРАММЫ')
async def part_1(message: types.Message):
    global zriteli_list
    global admin_id

    if zriteli_list:

        await bot.send_message(
            admin_id,
            'Началась часть первая: Телеграммы')

        await asyncio.sleep(93)
        for x in zriteli_list:
            await bot.send_message(x, config.TELEGRAM_LIST[0])
        await asyncio.sleep(48)
        for x in zriteli_list:
            await bot.send_message(x, config.TELEGRAM_LIST[1])
        await asyncio.sleep(50)
        for x in zriteli_list:
            await bot.send_message(x, config.TELEGRAM_LIST[2])
        await asyncio.sleep(6)
        for x in zriteli_list:
            await bot.send_message(x, config.TELEGRAM_LIST[3])
        await asyncio.sleep(55)
        for x in zriteli_list:
            await bot.send_message(x, config.TELEGRAM_LIST[4])
        await asyncio.sleep(40)
        for x in zriteli_list:
            await bot.send_message(x, config.TELEGRAM_LIST[5])
        await asyncio.sleep(62)
        for x in zriteli_list:
            await bot.send_message(x, config.TELEGRAM_LIST[8])
        await bot.send_message(admin_id, 'Запускай КОНЕЦ ТЕЛЕГРАММ!')
    else:
        await bot.send_message(
            admin_id,
            'Не хватает участников'
        )

## после окончания телеграм
@dp.message_handler(text='2. КОНЕЦ ТЕЛЕГРАММ')
async def after_part_1(message: types.Message):
    global zriteli_list
    global admin_id

    if zriteli_list:
        await bot.send_message(
            admin_id,
            'Переход между телеграммами и троллейбусом'
        )

        for x in zriteli_list:
            await bot.send_message(
                x,
                'Продолжим?\nЗайдите в троллейбус (следующий зал)')
        await asyncio.sleep(5)
        for x in zriteli_list:
            await bot.send_message(x, 'Ня')
        await asyncio.sleep(2)
        for x in zriteli_list:
            await bot.send_message(x, 'Мя')
        await asyncio.sleep(2)
        for x in zriteli_list:
            await bot.send_message(x, 'Тя')
        await asyncio.sleep(2)
        for x in zriteli_list:
            await bot.send_message(x, 'Я тя лю')
        await asyncio.sleep(2)
        for x in zriteli_list:
            await bot.send_message(x, 'А ти мя')
        await asyncio.sleep(2)
        for x in zriteli_list:
            await bot.send_message(x, 'Тчк')
        await asyncio.sleep(2)
        for x in zriteli_list:
            await bot.send_message(x, 'Пжлст')
        await asyncio.sleep(8)
        for x in zriteli_list:
            await bot.send_message(x, 'Ну')
        await asyncio.sleep(4)
        for x in zriteli_list:
            await bot.send_message(x, 'Я тя лю')
        await asyncio.sleep(2)
        for x in zriteli_list:
            await bot.send_message(x, 'А ти мя???')
        await asyncio.sleep(5)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Посмотри - все ли сели в троллейбус?\nМожем трогаться?\n\nЕсли да, то "осторожно, двери закрываются" - часть вторая\n#зиу9')
        await bot.send_message(
            admin_id,
            'Запускай часть вторую: ТРОЛЛЕЙБУС')
        turn_index()
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')


## запуск части с троллейбусом
@dp.message_handler(text='3. ТРОЛЛЕЙБУС')
async def part_2(message: types.Message):
    global zriteli_list
    global zritel_index
    global admin_id

    if zriteli_list:

        await bot.send_message(
            admin_id,
            'Началась часть вторая: Троллейбус')

        await asyncio.sleep(5)
        await bot.send_message(
            zriteli_list[zritel_index],
            'Поздравляю! С вашего устройства будет проигрываться эта аудиоисторя (файл придет тебе чуть позже).\nПодойдите к микрофону\n(он находится перед рулем троллейбуса).\n\nПоложите телефон рядом с микрофоном (там есть шпаргалка как это сделать)\nИ включите аудиозапись, которую я пришлю через некоторое время.\n\nНе забудь прибавить громкость телефона и класть его динамиком к микрофону')
        await asyncio.sleep(5)
        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ZIU9_voice_ID, 'Перед воспроизведением - возьмите внимание остальных зрителей!)')
        await bot.send_message(
            admin_id,
            'После окончания песни не забудь запустить: КОНЕЦ ТРОЛЛЕЙБУСА')
        turn_index()
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')

## после окончания троллейбуса
@dp.message_handler(text='4. КОНЕЦ ТРОЛЛЕЙБУСА')
async def after_part_2(message: types.Message):
    global zriteli_list
    global zritel_index
    global admin_id

    if zriteli_list:

        await bot.send_message(
            admin_id,
            'Переход между троллейбусом и комнатой')
        
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Кем бы я был, если бы был не ботом?')
        await asyncio.sleep(3)
        for x in zriteli_list:
            await bot.send_message(
                x, 
                'Я бы был уборщицей.\nС людьми не общаешься. Моешь пол и смотришь в свое отражение. Смотришь на себя каждый раз, как протрешь пол. Каждый раз, как протрешь всю пыль.\nКаждый раз, когда делаешь хотя бы небольшое усилие, ты видишь себя, свое лицо. Весь день делаешь так, чтобы все тебя увидели, все те, кто затопчут пол.\nОни не увидят себя в грязи.')
        await asyncio.sleep(12)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'А еще бы стал морем, чтобы все меня любили.')
        await asyncio.sleep(6)   
        for x in zriteli_list:
            await bot.send_message(
                x,
                'А кем бы были вы, если бы не были людьми?')
        await asyncio.sleep(12)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Продолжим? Вам надо дойти до следующей комнаты (ДЕНЬ ВТОРОЙ) и посмотреть телевизор.')
        await asyncio.sleep(20)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Все дошли до комнаты?\nЕсли так, то мне нужно вам кое-что объяснить!\n\nСейчас кому-то из вас будут приходить голосовые сообщения - их нужно включить.\nЭти сообщения - воспоминания одной девочки.\nПостарайтесь их расслышать.\nЕсли все готовы, то начинем третью часть:\n\n#напамять')
        await bot.send_message(
            admin_id,
            'Запускай часть третью: КОМНАТА первая')
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')

## часть комната первая##
@dp.message_handler(text='5. КОМНАТА первая')
async def part_3(message: types.Message):
    global zriteli_list
    global zritel_index
    global admin_id

    if zriteli_list:

        await bot.send_message(
            admin_id,
            'Началась часть третья: КОМНАТА первая')

        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ROOM_voice_1_ID,
            'воспоминание_1')
        turn_index()
        await asyncio.sleep(85)
        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ROOM_voice_2_ID,
            'воспоминание_2')
        turn_index()
        await asyncio.sleep(55)
        await bot.send_voice(
            zriteli_list[zritel_index], 
            config.ROOM_voice_3_ID,
            'воспоминание_3')
        turn_index()
        await asyncio.sleep(25)
        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ROOM_voice_4_ID,
            'воспоминание_4')
        turn_index()
        await bot.send_message(
            admin_id,
            'После слов:\n<i>"... теребит бороду и говорит"</i>\n\n<b>ВКЛЮЧИТЬ ВИДЕО №1</b>\n\nПосле видео запустить: КОМНАТА вторая')
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')

## комната вторая после видео
@dp.message_handler(text='6. КОМНАТА вторая')
async def part_3(message: types.Message):
    global zriteli_list
    global zritel_index
    global admin_id

    if zriteli_list:

        await bot.send_message(
            admin_id,
            'Продолжение третьей части: КОМНАТА вторая')
        
        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ROOM_voice_5_ID,
            'воспоминание_5')
        turn_index()
        await asyncio.sleep(60)
        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ROOM_voice_6_ID,
            'воспоминание_6')
        turn_index()
        await asyncio.sleep(75)
        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ROOM_voice_7_ID,
            'воспоминание_7')
        turn_index()
        await asyncio.sleep(40)
        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ROOM_voice_8_ID,
            'воспоминание_8')
        turn_index()
        await asyncio.sleep(60)
        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ROOM_voice_9_ID,
            'воспоминание_9')
        turn_index()

        await bot.send_message(
            admin_id,
            'После слов:\n<i>"... мам, что тебе надо?"</i>\n\n<b>ВКЛЮЧИТЬ ВИДЕО №2</b>\n\nПосле видео запустить: КОМНАТА третья')
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')

## комната третья после видео
@dp.message_handler(text='7. КОМНАТА третья')
async def part_3(message: types.Message):
    global zriteli_list
    global zritel_index
    global admin_id

    if zriteli_list:

        await bot.send_message(
            admin_id,
            'Продолжение третьей части: КОМНАТА третья')
        
        await bot.send_voice(
            zriteli_list[zritel_index],
            config.ROOM_voice_10_ID,
            'воспоминание_последнее')
        turn_index()

        await bot.send_message(
            admin_id,
            'После слов:\n<i>"... мам, что тебе надо?"</i>\n\n<b>ВКЛЮЧИТЬ ВИДЕО №3</b>\n\nПосле того, как на видео упала статуэтка - запустить: КОНЕЦ КОМНАТЫ')
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')

## после комнаты
@dp.message_handler(text='8. КОНЕЦ КОМНАТЫ')
async def after_part_3(message: types.Message):
    global zriteli_list
    global zritel_index
    global admin_id

    if zriteli_list:

        await bot.send_message(
            admin_id,
            'Переход между комнатой и войной')

        for x in zriteli_list:
            await bot.send_message(
                x,
                'Уважаемые дамы и господа! Уважаемые телезрители и телезрительицы! Уважаемые пользователи и пользовательницы! Пока вы идете в следующую комнату воспоминаний, я бы хотел задать вам несколько вопросов.')
        await asyncio.sleep(6)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'За каждый ответ вам будут начисляться баллы. Тот из вас, кто наберет наибольшее количество баллов, получит аааааааавтомобиль!')
        await asyncio.sleep(5)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'А пока войдите В ДВЕРЬ! и пройдите до зала "ПЯТЫЙ ДЕНЬ" (через зал ТРЕТИЙ ДЕНЬ и через зал ЧЕТВЕРТЫЙ ДЕНЬ)')
        await asyncio.sleep(8)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'И первый вопрос, уважаемые знатоки!')
        await asyncio.sleep(5)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Сколько вам было лет в 1991 году?')
        await asyncio.sleep(15)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Сколько вам было лет в 1999 году?')
        await asyncio.sleep(15)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Вы получали еду по талонам?')
        await asyncio.sleep(15)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Вы стояли в очереди за “Ножками Буша”?')
        await asyncio.sleep(15)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Вы участвовали в митингах?')
        await asyncio.sleep(15)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Вы боялись выйти из дома?')
        await asyncio.sleep(15)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Вы собирали наклейки из жвачек по рублю?')
        await asyncio.sleep(15)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Вы брали кассеты в видеопрокате?')
        await asyncio.sleep(15)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Вы хотели бы вернуться туда?')
        await bot.send_message(
            admin_id,
            'Запускай четвертую часть: ВОЙНА')
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')

## четвертая часть: война
@dp.message_handler(text='9. ВОЙНА')
async def part_4(message: types.Message):
    global zriteli_list
    global zritel_index
    global admin_id

    if zriteli_list:
    
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Вопросы были сложные.\nВы честно ответили на все вопросы и получили больше всех баллов.\nНо какое это все имеет значение?\nСейчас вы в музее.\nИ здесь и сейчас аааааавтомобиль вам не нужен.')
        await asyncio.sleep(8)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Здесь и сейчас вы стоите перед экраном.\nЗдесь и сейчас вам надо подойти к микрофону и прочитать строчки текста, которые придут вам в сообщении. \nИдите к микрофону в том случае, если вам пришли <i>ВАШИ СТРОЧКИ ТЕКСТА</i>')
        await asyncio.sleep(13)
        # стих
        await bot.send_message(zriteli_list[zritel_index], "<i>ВАШИ СТРОЧКИ ТЕКСТА:</i>\n\n\n<b>26 ноября 1994 года\n12 декабря 1994 года\n29 июля 1996 года\nв середине декабря\n6 августа 1996 года\n25 ноября 1994 года\nначалась война.\nслышались странные незнакомые звуки\nвезде пахло войной\nшла повсеместная вечная война\nв мире нет ничего, кроме войны,\nкроме Чечни</b>",)
        await asyncio.sleep(1)
        turn_index()

        await bot.send_message(
            admin_id,
            'После того как человек произнесет строки\n\n<i>"...в мире нет ничего, кроме войны,кроме Чечни"</i>\n\n<b>Запускай: СТИХ</b>'
        )
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')

## смена частей стихотворения
@dp.message_handler(text='10. СТИХ')
async def part_4(message: types.Message):
    global zriteli_list
    global zritel_index
    global voina_index
    global admin_id

    if zriteli_list:

        if voina_index < len(config.VOINA_LIST):
            await bot.send_message(
                zriteli_list[zritel_index],
                '<i>ВАШИ СТРОЧКИ ТЕКСТА:</i>\n\n\n<b>' + config.VOINA_LIST[voina_index] + '</b>')
            await bot.send_message(
                admin_id,
                'После текста\n\n\n<i>"' + config.VOINA_LIST[voina_index] + '"</i>\n\nЗапусти вновь: СТИХ')
            await asyncio.sleep(1)
            voina_index = voina_index + 1
            turn_index()
        else:
            await bot.send_message(
                admin_id,
                'Стих закончен.\n\nПосле звучащих в записи слов: <i>"...мы неузнали даже\nсовсем не узнали"</i>\n\nЗапусти: КОНЕЦ ВОЙНЫ')
            voina_index = 1
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')

## между войной и свободой
@dp.message_handler(text='11. КОНЕЦ ВОЙНЫ')
async def after_part_4(message: types.Message):
    global zriteli_list
    global zritel_index
    global admin_id

    if zriteli_list:

        await bot.send_message(
            admin_id,
            'Переход между войной и свободой')

        for x in zriteli_list:
            await bot.send_message(
                x,
                'Пройдите, пожалуйста дальше!\nВам нужно дойти до ЗАЛА СВОБОДЫ\nВы можете пройти туда как обычно - через зал ШЕСТОЙ ДЕНЬ, затем через зал СЕДЬМОЙ ДЕНЬ. Но так дольше и темнее (у нас не хватило времени и прожекторов)\nВы всегда можете посветить себе путь фонариками ваших телефонов')
        await asyncio.sleep(10)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'А можете сократить путь и дойти до ЗАЛА СВОБОДЫ напрямую.\nОбсудите этот вопрос и отправляйтесь к финальной части спектакля')
        await asyncio.sleep(8)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Пока вы обсуждаете, вспомнил анекдоты...\n\nТоварищи! Мы догоним и перегоним Америку по товарам народного потребления!\n- Голос из зала: Перегонять не надо!\n- А почему?\n- Голая жопа будет тогда видна!')
        await asyncio.sleep(15)  
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Еще один!\n\nДенег в казне нет, Ельцин созывает всех министров, спрашивает, что делать.\nЕму говорят:\n-Да вот тут Кока-Кола предлагает дать очень много денег. Только, Борис Николаевич, за это они просят на 10 лет сделать флагом России их логотип.\n- А много денег?\n Очень! \n- А когда у нас заканчивается контракт с Блендаметом?')
        await asyncio.sleep(12)
        for x in zriteli_list:
            await bot.send_message(
                x, 
                'Анекдотов тогда ходило! Огого! Не то, что нынешние мемы!\n\n- У вас есть дор блю?\n- А это что?\n- Это сыр с плесенью.\n- Сыра нет. Есть сосиски дор блю и картошка дор блю.\n\n\nНа уроке в школе детей новых русских учительница говорит:\nДети, кто купил домашнее задание, поднимите, пожалуйста, пальцы!')
        await asyncio.sleep(12)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Говорят, что смех освобождает...\n\nЗачем я это помню?')
        await asyncio.sleep(3)
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Жду вас в зале свободы... у центральной колонны')
        await bot.send_message(
            admin_id,
            'Запускай: СВОБОДА')
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')

## последняя часть свобода
@dp.message_handler(text='12. СВОБОДА')
async def part_5(message: types.Message):
    global zriteli_list
    global zritel_index
    global admin_id

    if zriteli_list:

        await bot.send_message(
            admin_id,
            'Началась последняя часть: СВОБОДА'
        )


        for x in zriteli_list:
            await bot.send_message(x, 'Все здесь? Тогда начинаем последнюю часть:\n#освободе')
        await asyncio.sleep(3)

        await bot.send_message(
            admin_id,
            'Запускай ВИДЕО "О свободе"\n\nВ конце, когда у избитого вновь спрашивают про свободу - запускай: ФИНАЛ'
        )
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')



## финал - удаляются все участники из users.json
@dp.message_handler(text='13. ФИНАЛ')
async def final(message: types.Message):
    global zriteli_list
    global zritel_index
    global start_set
    global admin_id
    global voina_index

    if zriteli_list:
        for x in zriteli_list:
            await bot.send_message(
                x,
                'Спектакль закончится только тогда, когда вы найдете новое определение слову “Свобода”.\nВписывайте свое определение прямо сюда.\nКогда новое определение будет найдено, я сообщу вам об этом.')
        empty_dict = {}
        with open('users.json', 'w') as empty_file:
            json.dump(empty_dict, empty_file)
        zritel_index = 0
        zriteli_list = []
        start_set = set()
        voina_index = 1
    else:
        await bot.send_message(
        admin_id,
        'Не хватает участников')


@dp.message_handler(content_types='text')
async def scan_message(message: types.Message):
    global zriteli_list
    global start_set

    with open('users.json', 'r') as file:
        check_users = json.load(file)
    if str(message.from_user.id) not in check_users and str(message.from_user.id) not in zriteli_list and str(message.from_user.id) not in start_set:
        await bot.send_message(
            message.from_user.id,
            'ПОВТОР!!!\nСпектакль не закончится, пока вы не не найдете уникальное определение!\n\n"Что такое свобода лично для Вас?"'
        )
    else:
        pass

### главный цикл
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)