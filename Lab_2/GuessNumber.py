def main():
    """
    Ввод значений с клавиатуры для формирования
    списка, по которому мы ищем искомое число и
    искомого числа
    (опционально) предложить пользователю сформировать
    список вручную с клавиатуры

    __вызов функции guess-number с параметрами: __
      - искомое число (target)
      - список, по-которому идем
      - тип поиска (последовательный, бинарный)

    __вывод результатов на экран__
    :return:
    """

    target = int(input('Введите target: '))
    diap = sorted(list(map(int,input('Введите числа интервала через пробел: ').split())))
    print(f'Ваш отсортированный диапазон: {diap}')
    res = guess_number(target, diap, type='bin')
    print(f'{res}')


def guess_number(target, lst, type='seq') -> list[int, int | None]:
    if type == 'seq':
        # ищем число последовательно
        for i in range(len(lst)):
            if lst[i] == target:
                return [target,i+1]
    elif type == 'bin':
        # ищем число с помощью алгоритма бинарного поиска
        mid = len(lst)//2
        if lst[mid] == target:
            return [target,1]
        elif lst[mid] < target:
            mid =

if __name__ == '__main__':
    pass
    main()