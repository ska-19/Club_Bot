function href_main(userId) {
    window.location.href = `/pages/main_user/${userId}`
}

function reject_user(productId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const RejProduct = {
        id: productId,
        user_id: 0,
        name: "",
        price: 0,
        description: "",
        quantity: 0
    }
    fetch(`/pages/history_user/${userId}/2`, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(RejProduct),
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

function accept(productId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const AccProduct = {
        id: productId,
        user_id: 0,
        name: "",
        price: 0,
        description: "",
        quantity: 0
    }
    fetch(`/pages/history_user/${userId}`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(AccProduct),
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

function reject_admin(productId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const RejProduct = {
        id: productId,
        user_id: 0,
        name: "",
        price: 0,
        description: "",
        quantity: 0
    }
    fetch(`/pages/history_user/${userId}/1`, {
        method: 'DELETE', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(RejProduct),
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

function checkHist(){
    document.getElementById(`History`).style.display = 'block';
    document.getElementById(`BtnHistory`).style.display = 'none';
}