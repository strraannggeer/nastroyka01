rng = range(1, 10, 2)
print(rng)

# Вывод в терминал: range(1, 10, 2)
# А где числа-то?

print(rng[3])

movies = ['Матрица', 'Хакеры', 'Трон', 'Тихушники', 'Сеть']
movie_ratings = [4.7, 5.0, 4.3, 4.9, 3.4]

# В качестве верхней границы диапазона
# передаётся длина списка movies.
print('Рейтинг пользователей')
for index in range(len(movies)):
    print(movies[index]+':', movie_ratings[index])