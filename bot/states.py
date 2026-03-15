from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    username = State()
    
class Change(StatesGroup):
    username = State()
    
class ReadUID(StatesGroup):
    ban = State()
    unban = State()
    queue = State()
    
class Discipline(StatesGroup):
    add = State()
    remove = State()
    rename = State()