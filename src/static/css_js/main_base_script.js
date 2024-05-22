function regForm() {
    document.querySelector('.RegEvent').style.display = 'none';
    document.querySelector('.DisregEvent').style.display = 'inline';
    document.querySelectorAll('input, textarea').forEach(input => input.removeAttribute('readonly'));
}

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

    fetch(`/pages/main_user/${userId}`, {
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