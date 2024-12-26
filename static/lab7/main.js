function fillFilmList() {
    // Отправляем GET-запрос на сервер для получения списка фильмов
    fetch('/lab7/rest-api/films/')
        .then(response => response.json()) // Преобразуем ответ сервера в JSON
        .then(films => {
            // Получаем элемент таблицы, где будет отображён список фильмов
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = ''; // Очищаем таблицу перед добавлением новых данных

            // Обрабатываем каждый фильм из полученного массива
            films.forEach((film, i) => {
                let tr = document.createElement('tr'); // Создаём строку таблицы для каждого фильма

                // Создаём ячейки для русского названия, названия на английском, года и действий
                let tdTitleRus = document.createElement('td'); // Ячейка для русского названия
                let tdTitle = document.createElement('td');    // Ячейка для английского названия
                let tdYear = document.createElement('td');     // Ячейка для года выпуска
                let tdActions = document.createElement('td');  // Ячейка для кнопок действий

                // Заполняем ячейку русского названия
                tdTitleRus.innerText = film.title_ru;

                // Если английское название есть, добавляем его в ячейку с курсивом, иначе оставляем пустым
                tdTitle.innerHTML = film.title ? `<i>(${film.title})</i>` : '';

                // Заполняем ячейку с годом выпуска фильма
                tdYear.innerText = film.year;

                // Создаём кнопку для редактирования фильма
                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать'; // Текст кнопки
                editButton.onclick = () => editFilm(film.id); // Привязываем функцию редактирования к кнопке

                // Создаём кнопку для удаления фильма
                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить'; // Текст кнопки
                delButton.onclick = () => deleteFilm(film.id, film.title_ru); // Привязываем функцию удаления к кнопке

                // Добавляем кнопки действий в ячейку
                tdActions.append(editButton);
                tdActions.append(delButton);

                // Добавляем все ячейки в строку таблицы
                tr.append(tdTitleRus, tdTitle, tdYear, tdActions);

                // Добавляем строку в таблицу
                tbody.append(tr);
            });
        });
}


function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) return;

    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ _method: 'DELETE' }) // Указываем метод
    })
    .then(() => fillFilmList())
    .catch(err => alert(`Ошибка при удалении фильма: ${err}`));
}


function showModal() {
    // Устанавливаем отображение модального окна (видимым)
    document.querySelector('.modal').style.display = 'block';

    // Очищаем текст всех элементов с классом 'error-message' (очистка сообщений об ошибках)
    document.querySelectorAll('.error-message').forEach(e => e.innerText = '');
}


function hideModal() {
    // Скрываем модальное окно, изменяя его стиль на "none"
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    // Вызываем функцию hideModal для закрытия модального окна
    hideModal();
}


function addFilm() {
    // Очищаем поля модального окна для создания нового фильма
    document.getElementById('id').value = ''; // Сбрасываем ID
    document.getElementById('title').value = ''; // Сбрасываем английское название
    document.getElementById('title-ru').value = ''; // Сбрасываем русское название
    document.getElementById('year').value = ''; // Сбрасываем год выпуска
    document.getElementById('description').value = ''; // Сбрасываем описание
    showModal(); // Отображаем модальное окно
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}/`) // Добавьте слеш в конце, если требуется
        .then(response => {
            if (!response.ok) throw new Error(`Ошибка при получении фильма: ${response.status}`);
            return response.json();
        })
        .then(film => {
            document.getElementById('id').value = film.id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        })
        .catch(err => alert(err));
}


function sendFilm() {
    // Получаем ID фильма из поля ввода (если ID есть, то это редактирование, иначе — создание)
    const id = document.getElementById('id').value;

    // Собираем данные фильма из полей ввода
    const film = {
        title: document.getElementById('title').value.trim(), // Английское название фильма
        title_ru: document.getElementById('title-ru').value.trim(), // Русское название фильма
        year: document.getElementById('year').value, // Год выпуска
        description: document.getElementById('description').value.trim() // Описание фильма
    };

    // Определяем URL и метод в зависимости от наличия ID
    const url = id ? `/lab7/rest-api/films/${id}` : '/lab7/rest-api/films/'; // URL: для PUT (обновление) или POST (создание)
    const method = id ? 'PUT' : 'POST'; // HTTP-метод: PUT для обновления, POST для создания

    // Отправляем запрос на сервер
    fetch(url, {
        method: method, // Устанавливаем HTTP-метод
        headers: { 'Content-Type': 'application/json' }, // Указываем тип данных JSON
        body: JSON.stringify(film) // Преобразуем объект фильма в строку JSON
    })
    .then(response => {
        if (response.ok) {
            hideModal(); // Если запрос успешен, скрываем модальное окно
            fillFilmList(); // Обновляем список фильмов
        }
        return response.json(); // Преобразуем ответ в JSON для обработки ошибок
    })
    .then(errors => {
        if (errors) {
            // Если сервер вернул ошибки, отображаем их под соответствующими полями ввода
            if (errors.title_ru) document.getElementById('title-ru-error').innerText = errors.title_ru; // Ошибка русского названия
            if (errors.year) document.getElementById('year-error').innerText = errors.year; // Ошибка года выпуска
            if (errors.description) document.getElementById('description-error').innerText = errors.description; // Ошибка описания
        }
    });
}
