

function getServices() {
    fetch("/api/services").then(res => res.json()).then(data => {
        let select = document.getElementById("select-service");
        for (service of data) {
            let option = new Option(service['name']);
            option.id = service["id"];
            option.dataset.price = service["price"];
            select.appendChild(option);
        }
    })
}