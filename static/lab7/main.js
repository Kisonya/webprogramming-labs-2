function fillFilmList() {
    console.log("Запрос на получение списка фильмов...");

    fetch('/lab7/rest-api/films/')
        .then(response => {
            if (!response.ok) throw new Error(`Ошибка при получении списка фильмов: ${response.status}`);
            return response.json();
        })
        .then(films => {
            console.log(`Список фильмов успешно получен:`, films);

            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            films.forEach(film => {
                let tr = document.createElement('tr');

                let tdTitleRus = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitleRus.innerText = film.title_ru;
                tdTitle.innerHTML = film.title ? `<i>(${film.title})</i>` : '';
                tdYear.innerText = film.year;

                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';
                editButton.onclick = () => editFilm(film.id);

                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';
                delButton.onclick = () => deleteFilm(film.id, film.title_ru);

                tdActions.append(editButton);
                tdActions.append(delButton);

                tr.append(tdTitleRus, tdTitle, tdYear, tdActions);
                tbody.append(tr);
            });
        })
        .catch(err => {
            console.error("Ошибка при получении списка фильмов:", err);
            alert(`Ошибка при получении списка фильмов: ${err.message}`);
        });
}


function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) return;

    console.log(`Запрос на удаление фильма с ID: ${id}, Название: "${title}"`);

    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE', // Используется HTTP-метод DELETE
    })
        .then(response => {
            if (!response.ok) throw new Error(`Ошибка при удалении фильма: ${response.status}`);
            console.log(`Фильм с ID ${id} успешно удалён.`);
            fillFilmList(); // Обновляем список фильмов
        })
        .catch(err => {
            console.error(`Ошибка при удалении фильма с ID ${id}:`, err);
            alert(`Ошибка при удалении фильма: ${err.message}`);
        });
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
    console.log(`Запрос на получение данных фильма с ID: ${id}`);

    fetch(`/lab7/rest-api/films/${id}`) // Убедитесь, что маршрут без завершающего "/"
        .then(response => {
            if (!response.ok) throw new Error(`Ошибка при получении фильма: ${response.status}`);
            return response.json();
        })
        .then(film => {
            console.log(`Данные фильма получены:`, film);

            // Заполняем модальное окно данными фильма
            document.getElementById('id').value = film.id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        })
        .catch(err => {
            console.error(`Ошибка при запросе фильма с ID ${id}:`, err);
            alert(`Ошибка при получении фильма: ${err.message}`);
        });
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
