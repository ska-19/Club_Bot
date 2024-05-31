function href_main(userId) {
    window.location.href = `/pages/main_user/${userId}`
}

function Begin() {
    document.getElementById(`CreateProductForm`).style.display = 'flex'
    document.getElementById(`CloseProduct`).style.display = 'flex'
    document.getElementById(`BeginProduct`).style.display = 'none'
}

function Close() {
    document.getElementById(`CreateProductForm`).style.display = 'none'
    document.getElementById(`CloseProduct`).style.display = 'none'
    document.getElementById(`BeginProduct`).style.display = 'flex'
    document.getElementById(`NameNewProduct`).value = ""
    document.getElementById(`PriceNewProduct`).value = ""
    document.getElementById(`DescriptionNewProduct`).value = ""
    document.getElementById(`QuantityNewProduct`).value = ""

}

function CreateProduct() {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const add_product_data = {
        name: document.getElementById(`NameNewProduct`).value,
        price: document.getElementById(`PriceNewProduct`).value,
        user_id: userId,
        description: document.getElementById(`DescriptionNewProduct`).value,
        quantity: document.getElementById(`QuantityNewProduct`).value,
        club_id: 1
    }
    fetch(`/pages/market_user/${userId}/1`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(add_product_data),
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

function Edit(productId) {
    document.querySelectorAll('.EditProduct').forEach(edit_button => edit_button.disabled = true)
    document.querySelectorAll('.EndProduct').forEach(end_button => end_button.disabled = true)
    document.getElementById(`SaveProduct_${productId}`).disabled = false
    document.getElementById(`EditProduct_${productId}`).style.display = 'none'
    document.getElementById(`SaveProduct_${productId}`).style.display = 'inline'
    document.getElementById(`NameProduct_${productId}`).removeAttribute('readonly')
    document.getElementById(`DescriptionProduct_${productId}`).removeAttribute('readonly')
    document.getElementById(`QuantityProduct_${productId}`).removeAttribute('readonly')
    document.getElementById(`PriceProduct_${productId}`).removeAttribute('readonly')

}

function Save(productId) {
    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');
    const userId = urlParts[urlParts.length - 1];
    const UpdateProductData = {
        id: productId,
        user_id: userId,
        name: document.getElementById(`NameProduct_${productId}`).value,
        price: document.getElementById(`PriceProduct_${productId}`).value,
        description: document.getElementById(`DescriptionProduct_${productId}`).value,
        quantity: document.getElementById(`QuantityProduct_${productId}`).value
    };
    fetch(`/pages/market_user/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(UpdateProductData),
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

function End(productId) {
    const currentUrl = window.location.href;
    const urlParts = currentUrl.split('/');
    const userId = urlParts[urlParts.length - 1];
    const DeleteProductData = {
        id: productId,
        user_id: 0,
        name: "",
        price: 0,
        description: "",
        quantity: 0
    };
    fetch(`/pages/market_user/${userId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(DeleteProductData),
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

function Buy(productId) {
    const urlParts = window.location.href.split('/');
    const userId = urlParts[urlParts.length - 1];
    const BuyProduct = {
        id: productId,
        user_id: 0,
        name: "",
        price: 0,
        description: "",
        quantity: 0
    }
    console.log(BuyProduct);
    fetch(`/pages/market_user/${userId}/2`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(BuyProduct),
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