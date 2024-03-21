let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#2cab37';

let item = "";

const userData = {
    user_id: tg.initDataUnsafe.user.id,
    first_name: tg.initDataUnsafe.user.first_name,
    last_name: tg.initDataUnsafe.user.last_name,
    info: ''
};

function saveUserInfo() {
    userData.info = document.getElementById('InputUserInfo').value();
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    } else {
        tg.MainButton.setText("Ваши изменения сохранены");
        item = "3";
        tg.MainButton.show();
    }
}

const dataToSend = {
    user_id: userData.user_id,
    message: userData.info
}
Telegram.WebApp.onEvent("mainButtonClicked", function () {
    tg.sendData(userData);
});

// Обработчик события перед закрытием окна или веб-страницы
window.addEventListener('beforeunload', function (event) {
    const jsonData = JSON.stringify(userData);
    const blob = new Blob([jsonData], {type: 'application/json'});
    const link = document.createElement('a');

    link.href = URL.createObjectURL(blob);
    link.download = `user_${userData.user_id}_data.json`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
});

let usercard = document.getElementById("usercard");
let p = document.createElement("p");
document.getElementById("name").value = userData.last_name + " " + userData.first_name;
usercard.appendChild(p);

///////////////////////////////////////
//Далее функции для фронтенда, без использования тг
///////////////////////////////////////


//Изменение аватарки
function uploadAvatar() {
    const avatarInput = document.getElementById('avatar-input');
    const avatarImage = document.getElementById('avatar-image');
    const chooseText = document.getElementById('choose-text');

    avatarInput.addEventListener('change', function () {
        const file = this.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                avatarImage.src = e.target.result;
                avatarImage.style.display = 'block';
                chooseText.style.display = 'none';
                avatarInput.files = [file];
            };

            reader.readAsDataURL(file);
        }
    });

    avatarImage.addEventListener('click', function () {
        avatarInput.click();
    });

    avatarImage.addEventListener('dblclick', function () {
        avatarInput.value = null;
        avatarImage.src = '';
        avatarImage.style.display = 'none';
        chooseText.style.display = 'block';
    });
}

function editForm() {
    var inputs = document.querySelectorAll("input, textarea");
    inputs.forEach(function (input) {
        input.readOnly = false;
    });

    var editBtn = document.querySelector(".editBtn");
    editBtn.style.display = "none";

    var saveBtn = document.createElement("button");
    saveBtn.innerHTML = "Сохранить";
    saveBtn.classList.add("editBtn"); // добавляем класс для стилизации

    saveBtn.onclick = function () {
        inputs.forEach(function (input) {
            input.readOnly = true;
        });
        editBtn.style.display = "block";
        saveBtn.parentNode.removeChild(saveBtn);
    };

    editBtn.parentNode.appendChild(saveBtn);
}