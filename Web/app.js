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

let btn1 = document.getElementById("btn1");
let btn2 = document.getElementById("btn2");
let btn4 = document.getElementById("btn4");

btn1.addEventListener("click", function () {
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    } else {
        tg.MainButton.setText("Вы выбрали котика 1!");
        item = "1";
        tg.MainButton.show();
    }
});

btn2.addEventListener("click", function () {
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    } else {
        tg.MainButton.setText("Вы выбрали супер котика 2!");
        item = "2";
        tg.MainButton.show();
    }
});

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
btn4.addEventListener("click", function () {
    tg.collapse();
});
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
usercard.appendChild(p);