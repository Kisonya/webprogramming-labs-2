function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = ''; // Очищаем таблицу

            films.forEach((film, i) => {
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
        });
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(() => fillFilmList()); // Обновляем список фильмов
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
    document.querySelectorAll('.error-message').forEach(e => e.innerText = '');
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
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
        .then(response => response.json())
        .then(film => {
            document.getElementById('id').value = film.id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        });
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title-ru').value.trim(),
        year: document.getElementById('year').value,
        description: document.getElementById('description').value.trim()
    };

    const url = id ? `/lab7/rest-api/films/${id}` : '/lab7/rest-api/films/';
    const method = id ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(film)
    })
    .then(response => {
        if (response.ok) {
            hideModal();
            fillFilmList();
        }
        return response.json();
    })
    .then(errors => {
        if (errors) {
            if (errors.title_ru) document.getElementById('title-ru-error').innerText = errors.title_ru;
            if (errors.year) document.getElementById('year-error').innerText = errors.year;
            if (errors.description) document.getElementById('description-error').innerText = errors.description;
        }
    });
}
