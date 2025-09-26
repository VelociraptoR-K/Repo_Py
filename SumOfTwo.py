"""Если более 1 ответа для индексов, то список из минимальных индексов в моей
   функции будет самым первым, поэтому сразу возвращаем результат."""
def sum_two(nums,target):
    if nums == [] or nums == None or target == None: # пустой список или нет ответа
        return None
    if len([el for el in nums if el==int(el)]) != len(nums): # все элементы должны быть целочисленными
        return None
    if type(target) != int: # переменная target должна быть целочисленной
        return None
    count = 1 # этот счётчик нужен для того, чтобы проход по циклу не начинался всё время с самого начала
    for i in range(len(nums)):
        for j in range(count, len(nums)): # начинаем сразу со следующего элемента
            if i != j and nums[i] + nums[j] == target:
                return [i,j]
        count += 1

res = sum_two([2,7,11,15], 9)
print(res)


