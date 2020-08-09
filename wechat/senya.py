from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


# 机器人函数
def chatbot(text):
    bot = ChatBot('senya',
            storage_adapter = "chatterbot.storage.SQLStorageAdapter",
            database = "botData.sqlite3"
                )
    '''
    # 可以通过yml文件对机器人进行训练，具体格式看xunlian文件夹
    train = ChatterBotCorpusTrainer(bot)
    train.train(
        'D:/wechat/xunlian'
        )
    '''
    response = bot.get_response(text)
    return response
