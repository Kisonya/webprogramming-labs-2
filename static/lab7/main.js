function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');

                let tdTitleRus = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitleRus.innerText = films[i].title_ru;
                tdTitle.innerHTML = films[i].title === films[i].title_ru
                    ? ''
                    : `<i>(${films[i].title})</i>`;
                tdYear.innerText = films[i].year;

                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';
                editButton.onclick = function () {
                    editFilm(i);
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';
                delButton.onclick = function () {
                    deleteFilm(i, films[i].title_ru);
                };

                tdActions.append(editButton);
                tdActions.append(delButton);

                tr.append(tdTitleRus);
                tr.append(tdTitle);
                tr.append(tdYear);
                tr.append(tdActions);

                tbody.append(tr);
            }
        });
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(function () {
            fillFilmList(); // Обновляем список фильмов после удаления
        });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
    clearErrors();
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function clearErrors() {
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function (data) {
            return data.json();
        })
        .then(function (film) {
            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        });
}

function sendFilm() {
    const id = document.getElementById('id').value;

    // Собираем данные фильма
    let title = document.getElementById('title').value.trim();
    let title_ru = document.getElementById('title-ru').value.trim();
    const year = document.getElementById('year').value.trim();
    const description = document.getElementById('description').value.trim();

    // Если оригинальное название пустое, но есть русское название, подставляем его
    if (title === '' && title_ru !== '') {
        title = title_ru;
    }

    // Подготавливаем объект с данными
    const film = {
        title: title,
        title_ru: title_ru,
        year: year,
        description: description
    };

    // Определяем URL и метод запроса
    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(film)
    })
    .then(function (resp) {
        return resp.json().then(function (data) {
            if (!resp.ok) {
                // Выводим ошибки на форму
                if (data.title_ru) {
                    alert(data.title_ru);
                }
                if (data.year) {
                    alert(data.year);
                }
                if (data.description) {
                    document.getElementById('description-error').innerText = data.description;
                }
                return;
            }
            fillFilmList();
            hideModal();
        });
    })
    .catch(function (error) {
        console.error('Ошибка:', error);
    });
}
