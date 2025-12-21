

function getServices() {
    fetch("/api/services").then(res => res.json()).then(data => {
        let select = document.getElementById("select-service");
        for (service of data) {
            let option = new Option(`${service['name']}: ${service['price'].toLocaleString('en-US', { maximumFractionDigits: 0 })} ₫`);
            option.id = service["id"];
            select.appendChild(option);
            let a = 10.5
        }
    })
}