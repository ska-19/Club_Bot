function href_main(userId) {
    window.location.href = `/pages/main_user/${userId}`
}

function Begin() {
    document.getElementById(`CreateEventForm`).style.display = 'flex'
    document.getElementById(`CloseEvent`).style.display = 'flex'
    document.getElementById(`BeginEvent`).style.display = 'none'
}

function Close() {
    document.getElementById(`CreateEventForm`).style.display = 'none'
    document.getElementById(`CloseEvent`).style.display = 'none'
    document.getElementById(`BeginEvent`).style.display = 'flex'
}

function CreateProduct() {
    console.log(EventReg)
    fetch(`/pages/market_user/${userId}/2`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(add_product),
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
