from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Inliner:

    def inline_maker(self, tasks):
        d = {}
        for i, j in enumerate(tasks, 0):
            d[f'button_{i+1}'] = j
        d = d.items()
        keyboard = InlineKeyboardMarkup()
        for q, p in d:
            button = InlineKeyboardButton(f'{p}', callback_data=f'{q}')
            keyboard.add(button)

        return keyboard



