const searchClub = () => {
    const search_club = document.getElementById("input_search").value;
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const found_uid = {
        uid: search_club
    }
    fetch(`/pages/search_user/${userId}/1`, {
        method: 'PUT', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(found_uid),
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

function ChangeMainClub(ClubId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const ClubData = {
        user_id: userId, club_id: ClubId
    }
    //TODO возможно переход на сёрч_юзер надо
    fetch(`/pages/search_user/${userId}/2`, {
        method: 'PUT', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(ClubData),
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

function LeaveClub(ClubId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const ClubData = {
        user_id: userId, club_id: ClubId
    }
    //TODO возможно переход на сёрч_юзер надо.что если главного нет????
    fetch(`/pages/search_user/${userId}`, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(ClubData),
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

function JoinClub(ClubId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const JoinData = {
        user_id: userId, club_id: ClubId, role: "member", balance: 0
    }
    //TODO сделать главным, переход хотелось бы в мейн
    fetch(`/pages/search_user/${userId}`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(JoinData),
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
            window.location.href = `/pages/main_user/${userId}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
