# config module for remember_bot_aio
import json

BOT_TOKEN = 'token' # change to your token
ADMIN_ID = 0 # change to your personal id

with open('start_message.json', 'r') as file:
    START_MESSAGE = json.load(file)

with open('telegramy.json', 'r') as telegram_file:
    TELEGRAM_LIST = json.load(telegram_file)

# аудио для зиу9
ZIU9 = open('media/ziu9.mp3', 'rb')
ZIU9_voice_ID = 'AwACAgIAAxkBAAIbZ2ENDuOtJEsTOd43dcnxDXsd9QMDAAIZDgACarZoSG2171KMTr9eIAQ'

# аудио для комнаты
ROOM_voice_1_ID = 'AwACAgIAAxkBAAIbmGENGPNgepfMkziA9fiWIpNlBbGAAAKGDgACarZoSNQJfXMM7pA4IAQ'
ROOM_voice_2_ID = 'AwACAgIAAxkBAAIbmWENGP2YEDr2PPEgZjEdU6uTcc_KAAKHDgACarZoSBmy8MoUW0S7IAQ'
ROOM_voice_3_ID = 'AwACAgIAAxkBAAIbmmENGQOWDJB-xsE6epgtkjuRI0nFAAKJDgACarZoSAey1WlEZ61bIAQ'
ROOM_voice_4_ID = 'AwACAgIAAxkBAAIbm2ENGQ246zYBWhumAaVVS4NrTEiOAAKKDgACarZoSDknzYTb4_1kIAQ'
ROOM_voice_5_ID = 'AwACAgIAAxkBAAIbqWENHv_pmaHWxey4Z4ITHQUUstDoAAKXDgACarZoSI3rRi26SyeNIAQ'
ROOM_voice_6_ID = 'AwACAgIAAxkBAAIbqmENHwd6XI0Rwovh57qZSKuP1CPTAAKYDgACarZoSDkZ9sSCm5RMIAQ'
ROOM_voice_7_ID = 'AwACAgIAAxkBAAIbq2ENHw_Ko1E1Hu2jXCUR98KeYSa-AAKaDgACarZoSNu6uNjhYdWPIAQ'
ROOM_voice_8_ID = 'AwACAgIAAxkBAAIbrGENHxdhUuc0y0CGp4plQMdDPMqJAAKbDgACarZoSN5qtu6PKFKFIAQ'
ROOM_voice_9_ID = 'AwACAgIAAxkBAAIbrWENHyK1OPjL1nAizLvXadID7ZOwAAKcDgACarZoSK_bKnY2Ur0DIAQ'
ROOM_voice_10_ID = 'AwACAgIAAxkBAAIbtWENInBpt7jwRwisKFHHnNnBRwsSAAKkDgACarZoSJ0L7ZKYPFkJIAQ'


# для стиха войны
with open('voina.json', 'r') as voina_file:
    VOINA_LIST = json.load(voina_file)
