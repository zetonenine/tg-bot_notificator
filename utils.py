from aiogram.dispatcher.filters.state import State, StatesGroup

class TestStates(StatesGroup):

    setting_task = State()


if __name__ == '__main__':
    print(TestStates.all())
