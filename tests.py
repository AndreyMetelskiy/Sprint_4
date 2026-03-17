import pytest
from main import BooksCollector

class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2
    
    # Проверка метода add_new_book: граничные значения длины названия (0, 1, 40, 41 символ)
    @pytest.mark.parametrize('name, expected_count', [
        ('', 0),                # Пустая строка: книга не должна быть добавлена
        ('A', 1),               # Минимально допустимая длина: успех
        ('A' * 40, 1),          # Максимально допустимая длина: успех
        ('A' * 41, 0)           # Превышение лимита символов: книга не добавляется
    ])
    def test_add_new_book_length_name(self, name, expected_count):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert len(collector.books_genre) == expected_count
    
    # Проверка метода set_book_genre: установка жанра при соблюдении условий (наличие в коллекции и в списке жанров)
    @pytest.mark.parametrize('name, genre, expected_result', [
        ('Есть', 'Ужасы', 'Ужасы'),    # Валидные данные: жанр успешно установлен
        ('Есть', 'Драма', ''),         # Жанра нет в списке разрешенных: значение не меняется
        ('Нет', 'Комедии', None),      # Книги нет в словаре: возврат None
        ('нет', "Боевик", None)        # Книги и жанра нет: возврат None
    ])
    def test_set_book_genre_conditions_true(self, name, genre, expected_result):
        collector = BooksCollector()
        collector.add_new_book('Есть')
        collector.set_book_genre(name, genre)
        assert collector.books_genre.get(name) == expected_result
    
    # Проверка метода get_book_genre: корректное получение установленного жанра
    def test_get_book_genre_return_genre(self):
        collector = BooksCollector()
        name = 'Чипполино и тайная комната'
        genre = 'Мультфильмы'
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.books_genre.get(name) == 'Мультфильмы'
        
    # Проверка метода get_books_with_specific_genre: фильтрация коллекции по конкретному жанру
    @pytest.mark.parametrize('books_to_add, specific_genre, expected_list', [
        # Возврат списка из нескольких книг одного жанра
        ([('Оно', 'Ужасы'), ('Сияние', 'Ужасы')], 'Ужасы', ['Оно', 'Сияние']),
        # Возврат только одной книги, соответствующей жанру
        ([('Дюна', 'Фантастика'), ('Дракула', 'Ужасы')], 'Фантастика', ['Дюна']),
        # Возврат пустого списка при отсутствии книг данного жанра
        ([('Дюна', 'Фантастика'), ('Сияние', 'Ужасы')], 'Комедии', [])
    ])
    def test_get_books_with_specific_genre_returns_expected_list(self, books_to_add, specific_genre, expected_list):
        collector = BooksCollector()
        for name, genre in books_to_add:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        result = collector.get_books_with_specific_genre(specific_genre)
        assert expected_list == result

    # Проверка метода get_books_genre: получение текущего состояния словаря книг
    @pytest.mark.parametrize('books_to_add, expected_result', [
        # Успешное получение словаря с несколькими записями
        ([('Оно', 'Ужасы'), ('Сияние', 'Ужасы')], {'Оно':'Ужасы', 'Сияние':'Ужасы'}),
        # Игнорирование некорректных названий (пустая строка)
        ([('Дюна', 'Фантастика'), ('', '')], {'Дюна':'Фантастика'}),
        # Отображение книг с не установленным жанром
        ([('Дюна', 'Фантастика'), ('Сияние', '')], {'Дюна':'Фантастика','Сияние': ''}),
        # Возврат пустого словаря при отсутствии валидных данных
        ([('', 'Фантастика')], {})    
    ])
    def test_get_books_genre_return_books_genre(self, books_to_add, expected_result):
        collector = BooksCollector()
        for name, genre in books_to_add:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        result = collector.get_books_genre()
        assert expected_result == result
    
    # Проверка метода get_books_for_children: исключение жанров с возрастным рейтингом
    @pytest.mark.parametrize('books_to_add, expected_result', [
        # Все добавленные книги подходят детям
        ([('Буратино', 'Комедии'), ('Сияние', 'Мультфильмы'), ('Шрек', 'Фантастика')], ['Буратино','Сияние','Шрек']),
        # Исключение книги с жанром 'Ужасы' (возрастной рейтинг)
        ([('Буратино', 'Комедии'), ('Сияние', 'Ужасы'), ('Шрек', 'Комедии')], ['Буратино','Шрек']),
        # Весь список состоит из книг с возрастным цензом
        ([('Дюна', 'Ужасы'), ('Сияние', 'Ужасы')], []),
        # Исключение книги без установленного жанра
        ([('Дюна', '')], [])    
    ])
    def test_get_books_for_children_return_filtration_is_correct(self, books_to_add, expected_result):
        collector = BooksCollector()
        for name, genre in books_to_add:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        result = collector.get_books_for_children()
        assert expected_result == result
        
    # Проверка метода add_book_in_favorites: возможность добавления только тех книг, которые есть в коллекции
    @pytest.mark.parametrize('books_genre, name, expected_result', [
        # Успешное добавление: книга существует в коллекции
        ({'Оно':'Ужасы', 'Сияние':'Ужасы'}, "Сияние", ["Сияние"]),
        # Неуспешное добавление: книга отсутствует в коллекции
        ({'Оно':'Ужасы', 'Сияние':'Ужасы'}, "Шрек", [])
    ])
    def test_add_book_in_favorites_only_if_book_exists_in_genre_list(self, books_genre, name, expected_result):
        collector = BooksCollector()
        collector.books_genre = books_genre
        collector.add_book_in_favorites(name)
        result = collector.favorites
        assert result == expected_result
        
    # Проверка метода add_book_in_favorites: исключение возможности повторного добавления (дублирования)
    @pytest.mark.parametrize('books_genre, name, favorites, expected_result', [
        # Книга добавлена впервые: список обновлен
        ({'Оно':'Ужасы', 'Сияние':'Ужасы'}, "Сияние", ["Оно"], ["Оно","Сияние"]),
        # Попытка повторного добавления: список не меняется
        ({'Оно':'Ужасы', 'Сияние':'Ужасы'}, "Сияние", ["Сияние"], ["Сияние"])
    ])
    def test_add_book_in_favorites_only_if_book_not_in_favorite_list(self, books_genre, name, favorites, expected_result):
        collector = BooksCollector()
        collector.books_genre = books_genre
        collector.favorites = favorites
        collector.add_book_in_favorites(name)
        result = collector.favorites
        assert result == expected_result
        
    # Проверка метода delete_book_from_favorites: удаление книги при её наличии в избранном
    @pytest.mark.parametrize('name, favorites, expected_result', [
        # Попытка удаления книги, которой нет в списке: список без изменений
        ("Сияние", ["Оно","Шрек"], ["Оно","Шрек"]),
        # Успешное удаление существующей книги
        ("Сияние", ["Оно","Шрек","Сияние"], ["Оно","Шрек"])
    ])
    def test_delete_book_from_favorites_only_if_book_in_favorite_list(self, name, favorites, expected_result):
        collector = BooksCollector()
        collector.favorites = favorites
        collector.delete_book_from_favorites(name)
        result = collector.favorites
        assert result == expected_result
        
    # Проверка метода get_list_of_favorites_books: корректность отображения текущего списка избранного
    @pytest.mark.parametrize('favorites, expected_result', [
        # Получение заполненного списка избранных книг
        (["Оно","Шрек"], ["Оно","Шрек"]),
        # Получение пустого списка, если избранное не заполнено
        ([], [])
    ])
    def test_get_list_of_favorites_books_correct_result(self, favorites, expected_result):
        collector = BooksCollector()
        collector.favorites = favorites
        result = collector.get_list_of_favorites_books()
        assert result == expected_result