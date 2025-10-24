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


<img width="640" height="480" alt="Figure_1" src="https://github.com/user-attachments/assets/3728d5dd-69db-452b-9689-3635d2d45c17" />


Сравнение НРекФакт (lru_cache) и НРекФакт n/a optimization


<img width="640" height="480" alt="Figure_23" src="https://github.com/user-attachments/assets/d66cfe0f-b8b3-4993-9dff-d4f16219da6d" />




