function Reg(eventId) {
    document.getElementById(`RegEvent_${eventId}`).style.display = 'none';
    document.getElementById(`DisregEvent_${eventId}`).style.display = 'inline';

    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const EventReg = {
        user_id: userId, event_id: eventId
    }

    fetch(`/pages/main_user/${userId}`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(EventReg),
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

function Disreg(eventId) {
    RegEvent = document.getElementById(`RegEvent_${eventId}`);
    DisregEvent = document.getElementById(`DisregEvent_${eventId}`);

    RegEvent.style.display = 'inline';
    DisregEvent.style.display = 'none';

    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const EventReg = {
        user_id: userId, event_id: eventId
    }
    fetch(`/pages/main_user/${userId}`, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(EventReg),
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

function Edit(eventId) {
    document.querySelectorAll('.EditEvent').forEach(edit_button => edit_button.disabled = true)
    document.querySelectorAll('.EndEvent').forEach(end_button => end_button.disabled = true)
    document.getElementById(`SaveEvent_${eventId}`).disabled = false
    document.getElementById(`EditEvent_${eventId}`).style.display = 'none'
    document.getElementById(`SaveEvent_${eventId}`).style.display = 'inline'
    document.getElementById(`textarea_${eventId}`).removeAttribute('readonly')
    document.getElementById(`Date_${eventId}`).removeAttribute('readonly')
    document.getElementById(`Speaker_${eventId}`).removeAttribute('readonly')
}

function Save(eventId) {
    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');
    const userId = urlParts[urlParts.length - 1];
    const EventData = {
        club_id: eventId,
        host_id: 1,
        name: "",
        date: document.getElementById(`Date_${eventId}`).value,
        sinopsis: document.getElementById(`textarea_${eventId}`).value,
        contact: document.getElementById(`Speaker_${eventId}`).value,
        speaker: document.getElementById(`Speaker_${eventId}`).value
    };
    fetch(`/pages/main_user/${userId}`,{
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(EventData),
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

function End(eventId) {

}