

class Decoder:

    def dcdr(self, callback_query):
        ran = len(callback_query.message.reply_markup.inline_keyboard)
        for i in range(0, ran):
            if callback_query.message.reply_markup.inline_keyboard[i][0].callback_data == callback_query.data:
                return callback_query.message.reply_markup.inline_keyboard[i][0].text
