function EndEvent(eventId) {
    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');
    const userId = urlParts[urlParts.length - 2];
    const usersContainer = document.getElementById('users-container');
    const checkboxes = usersContainer.querySelectorAll('input[type="checkbox"]');
    const usersJSON = {};

    checkboxes.forEach(checkbox => {
        const userId = checkbox.getAttribute('data-user_id');
        usersJSON[userId] = checkbox.checked ? 1 : 0;
    });

    const Data = {
        users: usersJSON
    }
    console.log(usersJSON);
    console.log(Data);
    fetch(`/pages/endevent_user/${userId}/${eventId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(Data),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            window.location.href = `/pages/main_user/${userId}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });

}