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

                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                // Условие: если названия совпадают, оставить пустым
                tdTitle.innerText = films[i].title === films[i].title_ru ? '' : films[i].title;
                tdTitleRus.innerText = films[i].title_ru;
                tdYear.innerText = films[i].year;

                // Создание кнопок
                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';

                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';

                // Добавление кнопок в ячейку действий
                tdActions.append(editButton);
                tdActions.append(delButton);

                // Добавление ячеек в строку
                tr.append(tdTitle);
                tr.append(tdTitleRus);
                tr.append(tdYear);
                tr.append(tdActions);

                // Добавление строки в таблицу
                tbody.append(tr);
            }
        });
}
