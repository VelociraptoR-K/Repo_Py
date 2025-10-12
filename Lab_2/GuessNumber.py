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
    diap = sorted(list(map(int,input('Введите числа диапазона через пробел: ').split())))
    print(f'Ваш диапазон после сортировки: {diap}')
    res = guess_number(target, diap,search_type='bin')
    print(f'{res}')

def guess_number(target: int, lst:list, search_type: str ='seq') -> list[int, int | None]:
    if type(lst) != list:
        return 'На вход подан не список'
    try:
        target_int = int(target)
        if target_int != float(target):  # Проверяем, что число целое
            return 'На вход подано нецелое число'
    except (ValueError, TypeError):
        return 'Данную строку нельзя преобразовать к int'
    target = target_int
    if target != int(target):
        return 'На вход подано нецелое число'
    if lst == []:
        return 'На вход подан пустой список'
    if search_type != 'seq' and search_type != 'bin':
        return 'Некорректный ввод типа поиска.'
    if search_type == 'seq':
        # ищем число последовательно
        for i in range(len(lst)):
            if lst[i] == target:
                return [target,i+1]
    elif search_type == 'bin':
        # ищем число с помощью алгоритма бинарного поиска
        srez = lst[:]
        c = 0
        while srez:  # пока список не пустой
            c += 1
            mid = len(srez) // 2
            if srez[mid] == target:
                return [target, c]
            elif srez[mid] < target:
                srez = srez[mid:] # в большую сторону (правая половина)
            else:
                srez = srez[:mid] # в меньшую сторону (левая половина)
    return [target, None]

if __name__ == '__main__':
    main()
