import random
from utils import *


def cmd_roll(message, args):
    if len(args) < 1:
        return roll_dice(1, 6)
    if args[0] == 'help':
        return '''\
```Usage:

  !roll XdY or !roll XwY
  e.g.: !roll 5d6```'''
    return roll_dice_str(message, args)


def roll_dice(count, type):
    msg = ''
    sum = 0

    for _ in range(count):
        dice_roll = random.randrange(type) + 1
        sum += dice_roll
        msg += str(dice_roll) + '+'

    msg = msg[:-1]
    if count > 1:
        msg += '=' + str(sum)

    msg = '`rolling ' + str(count) + 'd' + str(type) + ' ...`\n```Result: ' + msg + '```'
    print(msg)
    return msg


def roll_dice_str(message, args):
    if len(args) != 1:
        return 'Not a valid !roll command. Try !roll help'

    if 'd' in args[0]:
        split = 'd'
    elif 'w' in args[0]:
        split = 'w'
    else:
        return 'Not a valid !roll command. Try !roll help'

    dice = args[0].split(split)

    if len(dice) != 2:
        return 'Not a valid !roll command. Try !roll help'

    if (not represents_int(dice[0])) or (not represents_int(dice[1])):
        return 'Not a valid !roll command. Try !roll help'

    count = int(dice[0])
    type = int(dice[1])

    return roll_dice(count, type)
