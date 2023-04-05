from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard(id_action, lottery_action):
    return InlineKeyboardMarkup([[InlineKeyboardButton('Id', callback_data=id_action),
                                  InlineKeyboardButton('Loteria', callback_data=lottery_action)]])


def lottery_menu_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton('DIADESORTE', callback_data='diadesorte'),
                                  InlineKeyboardButton('DUPLASENA', callback_data='duplasena'),
                                  InlineKeyboardButton('LOTOFACIL', callback_data='lotofacil')],
                                 [InlineKeyboardButton('LOTOMANIA', callback_data='lotomania'),
                                  InlineKeyboardButton('MEGASENA', callback_data='megasena'),
                                  InlineKeyboardButton('QUINA', callback_data='quina')],
                                 [InlineKeyboardButton('TIMEMANIA', callback_data='timemania'),
                                  InlineKeyboardButton('SUPER7', callback_data='supersete'),
                                  InlineKeyboardButton('+MILIONARIA', callback_data='supersete')]])
