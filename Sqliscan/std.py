#coding = 'utf-8'
import time
from termcolor import colored
from terminaltables import SingleTable

def stderr(message, end="\n"):
    """
    输出一个错误给用户
    :param message:
    :param end:
    :return:
    """
    symbol = colored("[ERR]","red")
    currenttime = colored("[{}]".format(time.strftime("%H:%M:%S")),"green")
    print("{}{}{}".format(symbol, currenttime,message),end=end)

def stdout(message, end="\n"):
    """
    输出一个信息给用户
    :param message:
    :param end:
    :return:
    """
    symbol = colored("[MSG]", "yellow")
    currentime = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    print("{} {} {}".format(symbol, currentime, message), end=end)

def stdin(message, params, upper=False, lower=False):
    """
    询问用户输入信息
    :param message:
    :param params:
    :param upper:
    :param lower:
    :return: 用户输入的信息
    """
    symbol = colored("[OPT]","magenta")
    currentime = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    option = input("{} {} {}: ".format(symbol, currentime, message))

    if upper:
        option =option.upper()
    elif lower:
        option = option.lower()

    while option not in params:
        option = input("{} {} {}: ".format(symbol, currentime, message))

        if upper:
            option = option.upper()
        elif lower:
            option = option.lower()

    return option

def showsign(message):
    """
    输出一个漏洞信息
    :param message:
    :return:
    """
    print(colored(message, "magenta"))


def fullprint(data):
    """
    输出漏洞网址的服务器信息
    :param data:
    :return:
    """

    # [
    #   ["index", "url", "db", server", "lang"],
    #   ["1", "sql.com", "mysql", apache", "php/5.5xxx"]
    # ]

    title = " VULNERABLE URLS "
    table_data = [["index", "url", "db", "server", "lang"]]
    # add into table_data by one by one
    for index, each in enumerate(data):
        table_data.append([index+1, each[0], each[1], each[2][0:30], each[3][0:30]])

    table = SingleTable(table_data, title)
    print(table.table)

if __name__ == '__main__':
    stderr('error')
    stdout("OK")
    showsign("vulnerable")
    stdin("do you want to continue scanning? [Y/N]", ["Y", "N"], upper=True)