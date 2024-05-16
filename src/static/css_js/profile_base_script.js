/*let tg = window.Telegram.WebApp;

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
usercard.appendChild(p);*/

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

//кнопка "Изменить"
function editForm() {
    console.log("Success");
    var inputs = document.querySelectorAll("input, textarea");
    inputs.forEach(function (input) {
        input.readOnly = false;
    });

    var editBtn = document.querySelector(".editBtn");
    editBtn.style.display = "none";

    var saveBtn = document.querySelector(".saveBtn");
    saveBtn.style.display = "inline-block";

    saveBtn.onclick = function () {
        inputs.forEach(function (input) {
            input.readOnly = true;
        });
        editBtn.style.display = "inline-block";
        saveBtn.style.display = "none";
    };
}

//Кнопка "Сохранить"
function saveUserInfo() {
    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');
    const userId = urlParts[urlParts.length - 1];
    const userData = {
        dob: document.getElementById('DateOfBirth').value,
        city: document.getElementById('City').value,
        education: document.getElementById('Education').value,
        bio: document.getElementById('textarea').value
    };

    console.log("userData:", userData);

    fetch(`/pages/profile_user/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function editForm() {
    document.querySelector('.editBtn').style.display = 'none';
    document.querySelector('.saveBtn').style.display = 'inline';
    document.querySelectorAll('input, textarea').forEach(input => input.removeAttribute('readonly'));
}
