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

                // Логика отображения оригинального названия
                let titleRus = films[i].title_ru;
                let title = films[i].title;
                tdTitleRus.innerText = titleRus;

                // Если оригинальное название присутствует и не совпадает с русским, показываем его в скобках
                if (title && title !== titleRus) {
                    tdTitle.innerHTML = `<i>(${title})</i>`;
                } else {
                    tdTitle.innerHTML = ''; // Если совпадает или пустое, ничего не показываем
                }

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
    document.getElementById('description-error').innerText = ''; // Очистка сообщения об ошибке
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
    const title = document.getElementById('title').value.trim();

    // Проверка: если оригинальное название пустое, копируем из русского названия
    let finalTitle = title;
    if (title === '' && titleRu !== '') {
        finalTitle = titleRu;
        document.getElementById('title').value = finalTitle; // Обновляем поле в форме
    }

    const film = {
        title: finalTitle,
        title_ru: titleRu,
        year: document.getElementById('year').value.trim(),
        description: document.getElementById('description').value.trim()
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
        // Отображение ошибок в форме
        if (errors.title_ru) {
            document.getElementById('title-ru-error').innerText = errors.title_ru;
        }
        if (errors.title) {
            document.getElementById('title-error').innerText = errors.title;
        }
        if (errors.year) {
            document.getElementById('year-error').innerText = errors.year;
        }
        if (errors.description) {
            document.getElementById('description-error').innerText = errors.description;
        }
    })
    .catch(function (error) {
        console.error('Ошибка:', error);
    });
}
