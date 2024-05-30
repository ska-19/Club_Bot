function Update(ChangedUserId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const UserData = {
        user_id: ChangedUserId, club_id: 0
    }
    console.log(UserData)
    fetch(`/pages/club_user/${userId}`, {
        method: 'PUT', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(UserData),
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


function Kick(ChangedUserId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const UserData = {
        user_id: ChangedUserId, club_id: 0
    }
    fetch(`/pages/club_user/${userId}`, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(UserData),
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

function GetStatistics(){

}