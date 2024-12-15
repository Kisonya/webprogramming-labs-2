function fillFilmList() {
    // Запрашиваем список фильмов с сервера
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            // Заполняем таблицу с фильмами
            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');

                let tdTitleRus = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitleRus.innerText = films[i].title_ru;
                tdTitle.innerHTML = films[i].title === films[i].title_ru || !films[i].title
                    ? ''  // Если оригинальное название совпадает с русским или пустое, не показываем
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
    document.getElementById('description-error').innerText = '';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
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
    const titleRu = document.getElementById('title-ru').value.trim();
    let title = document.getElementById('title').value.trim();

    // Если оригинальное название пустое, копируем русское название
    if (!title && titleRu) {
        title = titleRu;
    }

    const film = {
        title: title,
        title_ru: titleRu,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

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
        if (resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function (errors) {
        // Выводим ошибки, если они есть
        if (errors.title_ru) {
            alert(errors.title_ru);
        }
        if (errors.description) {
            document.getElementById('description-error').innerText = errors.description;
        }
    })
    .catch(function (error) {
        console.error('Ошибка:', error);
    });
}
