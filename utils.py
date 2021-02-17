from aiogram.dispatcher.filters.state import State, StatesGroup

class TestStates(StatesGroup):

    setting_task = State()


if __name__ == '__main__':
    print(TestStates.all())






# {"id": "1628208301575257987",
 # "from":
 #     {"id": 379096786,
 #      "is_bot": false,
 #      "first_name": "Andrey",
 #      "last_name": "Zaytsev",
 #      "username": "threenineteen319",
 #      "language_code": "ru"},
 # "message":
 #     {"message_id": 1810,
 #      "from":
 #          {"id": 1160891964,
 #           "is_bot": true,
 #           "first_name": "Tester",
 #           "username": "Tester_myskills_bot"},
 #      "chat": {"id": 379096786,
 #               "first_name": "Andrey",
 #               "last_name": "Zaytsev",
 #               "username": "threenineteen319",
 #               "type": "private"},
 #      "date": 1613379525,
 #      "text": "Что из задуманного ты сделал?",
 #      "reply_markup":
 #          {"inline_keyboard":
 #               [
 #                   [
 #                       {"text": "Поесть",
 #                        "callback_data": "button_1"}
 #                   ],
 #                   [
 #                       {"text": "Попить",
 #                        "callback_data": "button_2"}
 #                   ],
 #                   [
 #                       {"text": "Назначить задачу",
 #                        "callback_data": "button_3"}
 #                   ]
 #               ]
 #          }
 #      },
 # "chat_instance": "1330384033559837008", "data": "button_2"}
