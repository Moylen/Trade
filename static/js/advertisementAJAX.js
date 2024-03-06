const advList = document.querySelector('.js-advertisement')

const advertisementTemplate = (pk, title) => {
    return (
        `<div class="d-flex flex-column align-items-center">
            <div class="col-md-9">
                <div class="d-flex justify-content-between border p-3 mb-1">
                    <a class="d-flex align-items-center text-decoration-none me-2"
                        href="../product/${pk}">${title}</a>
                    <a href="../remove/${pk}" data-id="${pk}"
                        class="btn btn-danger d-flex align-items-center align-self-center js-delete-adv">Удалить</a>
                </div>
            </div>
         </div>`
    )
}

const renderAdvertisements = () => {
    let str = ''
    return (
        fetch('http://127.0.0.1:8000/v1/advertisements/get/')
            .then(response => response.json())
            .then(data => {
                data.forEach(el => {
                    str += advertisementTemplate(el.pk, el.fields.title)
                })
                advList.innerHTML = str;
            })
    )
}

const setDeleteEvents = () => {
    return new Promise((resolve) => {
        const deleteButtons = document.querySelectorAll('.js-delete-adv')
        deleteButtons.forEach((el) => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                fetch(`http://127.0.0.1:8000/v1/advertisements/delete/${e.target.dataset.id}`)
                    .then(() => renderAdvertisements());
            })
        })
    })
}

const useRender = () => {
    renderAdvertisements().then(() => {
        return setDeleteEvents();
    });
}

useRender();