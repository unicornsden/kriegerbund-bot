import random
from . import messages
from .utils import represents_int


def cmd_dice(message, args):
    """
    cmd switch for dice
    :param message: the message to read from
    :type message: messages.MessageWrapper
    :param args: command arguments
    :type args: list(str)
    :return:
    """
    if len(args) < 1:
        return roll_dice(1, 6)
    if args[0] == 'help':
        return messages.send_message(message, 'dice-help')
    return roll_dice_str(message, args)


def roll_dice(message, dice_count, dice_type, split='d'):
    msg = ''
    roll_sum = 0

    for _ in range(dice_count):
        dice_roll = random.randrange(dice_type) + 1
        roll_sum += dice_roll
        msg += str(dice_roll) + '+'

    msg = msg[:-1]
    if dice_count > 1:
        msg += '=' + str(roll_sum)

    msg = (messages.get_string('dice-roll-1')
    + str(dice_count) + split
    + str(dice_type) + messages.get_string('dice-roll-2') + msg
    + messages.get_string('dice-roll-3'))

    return messages.send_custom_message(message, msg)


def roll_dice_str(message, args):
    if len(args) != 1:
        return messages.MessageCode.UNKNOWN_ARGS
    if 'd' in args[0]:
        split = 'd'
    elif 'w' in args[0]:
        split = 'w'
    else:
        return messages.MessageCode.UNKNOWN_ARGS

    dice = args[0].split(split)

    if len(dice) != 2:
        return messages.MessageCode.UNKNOWN_ARGS

    if (not represents_int(dice[0])) or (not represents_int(dice[1])):
        return messages.MessageCode.UNKNOWN_ARGS

    dice_count = int(dice[0])
    dice_type = int(dice[1])

    return roll_dice(message, dice_count, dice_type, split)
