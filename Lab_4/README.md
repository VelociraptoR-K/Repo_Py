Сравнение 2 способами: 

Первый:

Сравнение lru_cache РекФакт и НРекФакт


<img width="640" height="480" alt="Figure_1" src="https://github.com/user-attachments/assets/8c0fe3ed-8ff3-40fc-a89c-b4a9ba6e3bf4" />


Вывод: Кэшированная функция вычисления рекурсивного факториала работает медленее, так как помимо вычислений ещё дополнительно тратит время на вызовы самой себя.

Сравнение n/a optimization РекФакт и НРекФакт️:


<img width="640" height="480" alt="Figure_3" src="https://github.com/user-attachments/assets/17b069ce-6b03-4542-90c2-c5ab9282b312" />


Вывод: Рекурcивный вариант вычисления факториала работает медленнее, так как помимо вычислений ещё дополнительно тратит время на вызовы самой себя.

Второй:

Сравнение РекФакт (lru_cache) и РекФакт n/a optimization


<img width="640" height="480" alt="Figure_1" src="https://github.com/user-attachments/assets/22a2108b-3857-4858-866b-d9c702441171" />



Вывод: Кэшированная рекурсивная функция работает намного быстрее просто рекурсивной, так как сохраняет результаты вычислений в кэш, позволяя обращаться к ним, не выполняя новых вычислений.

Сравнение НРекФакт (lru_cache) и НРекФакт n/a optimization


<img width="640" height="480" alt="Figure_2" src="https://github.com/user-attachments/assets/32ce7448-64ec-46a6-9196-9d71b43572f8" />





