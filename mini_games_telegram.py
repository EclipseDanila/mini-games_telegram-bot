import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

token = '5536915116:AAFWYrLY-DiudhsieMf1vXepa33Eq4emqBg'

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создание клавиатур начало
commands = [
    '/start',
    '/help',
    '/tic_tac_toe',
    '/bulls_cows',
]

commands_markup = ReplyKeyboardMarkup()
for command in commands:
    commands_markup.insert(KeyboardButton(command))

tic_tac_toe_markup = ReplyKeyboardMarkup()
for i in range(3):
    tic_tac_toe_markup.insert(str(i+1))

bulls_cows_markup = ReplyKeyboardMarkup()
for i in range(10):
    bulls_cows_markup.insert(str(9-i))
# Создание клавиатур конец


# Основные команды начало
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет!\nЧто бы посмотреть весь список комманд введите /help.", reply_markup=commands_markup)

@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.answer("Можно выбрать одну из комманд :)", reply_markup=commands_markup)
# Основные команды конец


# Крестики-нолики начало
class ticTacToeState(StatesGroup):
    isWin = State()
    arrey = State()
    steps = State()
    playerType = State()
    x = State()
    y = State()  

@dp.message_handler(commands=['tic_tac_toe'])
async def tic_tac_toe_start(message: types.Message, state: FSMContext):
    await message.answer('Для преждевременного завершения игры введите: "end" или "finish"')
    await message.answer("Ход игрока 'x'\nВведите строку: ", reply_markup=tic_tac_toe_markup)
    steps = 9
    playerType = 'x'
    isWin = True
    arrey = [
            ['1', '1', '1'],
            ['1', '1', '1'],
            ['1', '1', '1'],
    ]
    await state.update_data(arrey=arrey)
    await state.update_data(playerType=playerType)
    await state.update_data(steps=steps)
    await state.update_data(isWin=isWin)
    # Перейти к заполнению состояния x
    await ticTacToeState.x.set()
  
@dp.message_handler(state=ticTacToeState.x)
async def tic_tac_toe_y(message: types.Message, state: FSMContext):
    if message.text == 'end' or message.text == 'finish':
        await message.answer("Завершение игры ", reply_markup=commands_markup) 
        await state.finish()
        return
    await message.answer("Введите столбец: ")
    await state.update_data(x=message.text)
    # Перейти к заполнению состояния y
    await ticTacToeState.y.set() 

@dp.message_handler(state=ticTacToeState.y)
async def tic_tac_toe_main(message: types.Message, state: FSMContext):
    if message.text == 'end' or message.text == 'finish':
        await message.answer("Завершение игры ", reply_markup=commands_markup) 
        await state.finish()
        return
    await state.update_data(y=message.text)
    data = await state.get_data()
    if (data['x'].isdigit() and data['y'].isdigit()):
        x = int(data['x'])
        y = int(data['y'])

        arrey = data['arrey']

        if (x < 1 or x > 3 or y < 1 or y > 3):
            await message.answer('Данные заполнены неправильно!\nВведите строку: ')
            await ticTacToeState.x.set()
        else:
            if(arrey[x-1][y-1] == '1'):
                playerType = data['playerType']
                arrey[x-1][y-1] = playerType
                steps = int(data['steps'])
                steps-=1
                await state.update_data(steps=steps)
                await state.update_data(arrey=arrey)  
            else:
                await message.answer('Клетка занята\nВведите строку: ')
                await ticTacToeState.x.set()

            field = ''
            for i in range(3):
                field_row = ''
                for t in range(3):
                    field_row+= arrey[i][t] + ' '
                field+=field_row + '\n'
            await message.answer(field)


            isWin = data['isWin']
            for i in range(3):
                if(arrey[i][0] == arrey[i][1] == arrey[i][2] == playerType):
                    isWin = False
                if(arrey[0][i] == arrey[1][i] == arrey[2][i] == playerType):
                    isWin = False
            if(arrey[0][0] == arrey[1][1] == arrey[2][2] == playerType or arrey[0][2] == arrey[1][1] == arrey[2][0] == playerType):
                isWin = False
            if (steps == 0 and isWin == True):
                await message.answer('Ничья', reply_markup=commands_markup)
                await state.finish()
            elif (isWin):
                if(playerType == 'x'):
                    await state.update_data(playerType='y')
                    await message.answer("Ход игрока 'y'\nВведите строку: ")
                    await ticTacToeState.x.set()
                else:
                    await state.update_data(playerType='x')
                    await message.answer("Ход игрока 'x'\nВведите строку: ")
                    await ticTacToeState.x.set()
            else:
                await message.answer("Победил игрок: " + playerType, reply_markup=commands_markup)
                await state.finish()
    else:
        await message.answer('Нужно указывать только цифры или столбцы\nВведите строку: ')
        await ticTacToeState.x.set()
# Крестики-нолики конец     

# Быки и коровы начало
class bullsCowsState(StatesGroup):
    steps =  State()
    randArr =  State()
    userInt =  State()
    userArr = State()

@dp.message_handler(commands=['bulls_cows'])
async def bulls_cows_start(message: types.Message, state: FSMContext):
    await message.answer("Привет. Это игра Быки и коровы.\nВведите цифру: ", reply_markup=bulls_cows_markup)
    await message.answer('Для преждевременного завершения игры введите: "end" или "finish"')
    await state.update_data(isVictory=False)
    await state.update_data(steps=1)
    await state.update_data(userArr=[])

    randArr = []
    while len(randArr) < 4:
        a = round(random.random() * 9)
        if a in randArr:
            continue
        else:
            randArr.append(a)

    await state.update_data(randArr=randArr)
    await message.answer(randArr)
    
    await bullsCowsState.userInt.set()

@dp.message_handler(state=bullsCowsState.userInt)
async def tic_tac_toe_end(message: types.Message, state: FSMContext): 
    if message.text == 'end' or message.text == 'finish':
        await message.answer("Завершение игры ", reply_markup=commands_markup) 
        await state.finish()
        return
    data = await state.get_data()
    userArr = data['userArr']
    randArr = data['randArr']

    userInt = abs(int(message.text))
    if message.text.isdigit():
        if (len(userArr) < 3) and ((userInt > 9) or (userInt in userArr)):
            await message.answer('Число не должно быть больше 9\nА так же не должно повторяться.')
        elif (len(userArr) < 3) and ((userInt <= 9) and (not userInt in userArr)):
            userArr.append(userInt)
            await message.answer('Введите цифру: ')
            await state.update_data(userArr=userArr)
            await bullsCowsState.userInt.set()
        elif (len(userArr) == 3) and ((userInt <= 9) and (not userInt in userArr)):
            await message.answer('Мы получили ваш запрос')
            userArr.append(userInt)
            await state.update_data(userArr=userArr)

            bulls = 0
            cows = 0
            for userEl in userArr:
                for randEl in randArr:
                    if (userArr.index(userEl) == (randArr.index(randEl))) and (userEl == randEl):
                        bulls += 1
                    elif (userEl == randEl):
                        cows += 1

            if (userArr == randArr):
                await message.answer('Поздравляю вы победили!', reply_markup=commands_markup)
                await state.finish()
            else:
                await state.update_data(userArr=[])
                output = ''
                for el in userArr:
                    output+=str(el) + ' '
                await message.answer(output + '\nКоровы: ' + str(cows) +'\nБыки: ' + str(bulls))
                await message.answer('Введите число')
    else:
        await message.answer('Запрос должен состоять из одной цифры')
# Быки и коровы конец


if __name__ == '__main__':
    executor.start_polling(dp)
    