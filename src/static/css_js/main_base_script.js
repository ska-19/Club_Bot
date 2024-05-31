function Reg(eventId) {
    document.getElementById(`RegEvent_${eventId}`).style.display = 'none';
    document.getElementById(`DisregEvent_${eventId}`).style.display = 'inline';

    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const EventReg = {
        user_id: userId, event_id: eventId
    }

    fetch(`/pages/main_user/${userId}/1`, {
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
    document.getElementById(`Contact_${eventId}`).removeAttribute('readonly')
    document.getElementById(`Reward_${eventId}`).removeAttribute('readonly')
}

function Save(eventId) {
    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');
    const userId = urlParts[urlParts.length - 1];
    const EventData = {
        club_id: eventId,
        host_id: userId,
        name: "",
        date: document.getElementById(`Date_${eventId}`).value,
        sinopsis: document.getElementById(`textarea_${eventId}`).value,
        contact: document.getElementById(`Contact_${eventId}`).value,
        speaker: document.getElementById(`Speaker_${eventId}`).value,
        reward: document.getElementById(`Reward_${eventId}`).value
    };
    fetch(`/pages/main_user/${userId}`, {
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

function Begin() {
    document.getElementById(`CreateEventForm`).style.display = 'flex'
    document.getElementById(`CloseEvent`).style.display = 'flex'
    document.getElementById(`BeginEvent`).style.display = 'none'
}

function Close() {
    document.getElementById(`SinopsisNewEvent`).value = ""
    document.getElementById(`NameNewEvent`).value = ""
    document.getElementById(`DateNewEvent`).value = ""
    document.getElementById(`SpeakerNewEvent`).value = ""
    document.getElementById(`RewardNewEvent`).value = ""
    document.getElementById(`ContactNewEvent`).value = ""
    document.getElementById(`CreateEventForm`).style.display = 'none'
    document.getElementById(`CloseEvent`).style.display = 'none'
    document.getElementById(`BeginEvent`).style.display = 'flex'
}

function CreateEvent() {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const EventReg = {
        club_id: 1,
        host_id: userId,
        name: document.getElementById(`NameNewEvent`).value,
        date: document.getElementById(`DateNewEvent`).value,
        sinopsis: document.getElementById(`SinopsisNewEvent`).value,
        contact: document.getElementById(`ContactNewEvent`).value,
        speaker: document.getElementById(`SpeakerNewEvent`).value,
        reward: document.getElementById(`RewardNewEvent`).value
    }
    console.log(EventReg)
    fetch(`/pages/main_user/${userId}/2`, {
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

function End(eventId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    window.location.href = `/pages/endevent_user/${userId}/${eventId}`
}

function href_channel(link) {
    window.location.href = link
}

function href_market(userId) {
    window.location.href = `/pages/market_user/${userId}`
}