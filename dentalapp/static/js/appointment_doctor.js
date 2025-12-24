

function addService() {
    let select = document.getElementById("doctor-select-service");
    let name = select.options[select.selectedIndex].dataset.name;
    let price = select.options[select.selectedIndex].dataset.price;
    let id = select.options[select.selectedIndex].id.replace("option", "tr");
    // console.log(name);
    // console.log(price);
    // console.log(id);

    let tbody = document.getElementById("list-services");
    let row = document.createElement("tr");
    row.id = `${id}`;
    row.innerHTML = `
        <td>${name} (chỉ định thêm)</td>
        <td data-price="${parseFloat(price)}">${parseFloat(price).toLocaleString('en-US')} ₫</td>
        <td class="d-flex justify-content-center"><button class="btn btn-danger" onclick="deleteService('${id}');">Xoá</button></td>
    `;

    tbody.appendChild(row);

    tbody.dataset.total = `${parseFloat(tbody.dataset.total) + parseFloat(price)}`;
    document.getElementById("total-services").value = `Tổng tiên dịch vụ: ${parseFloat(tbody.dataset.total).toLocaleString("en-US")} ₫`;

    select.options[select.selectedIndex].disabled = true;
    select.selectedIndex = 0;
    console.log(id);
}

function deleteService(id) {
    let tbody = document.getElementById("list-services");
    let service = document.getElementById(id);

    tbody.dataset.total = `${parseFloat(tbody.dataset.total) - parseFloat(service.children[1].dataset.price)}`;
    document.getElementById("total-services").value = `Tổng tiên dịch vụ: ${parseFloat(tbody.dataset.total).toLocaleString("en-US")} ₫`;
    
    let option = document.getElementById(id.replace("tr", "option"));
    console.log(id);
    console.log(option);
    option.disabled = false;
    tbody.removeChild(service);
}

function addMedicine() {
    let select = document.getElementById("doctor-select-medicine");

    let name = select.options[select.selectedIndex].dataset.name;
    let price = select.options[select.selectedIndex].dataset.price;
    let id = select.options[select.selectedIndex].id.replace("option", "tr");

    let tbody = document.getElementById("list-medicines");
    let row = document.createElement("tr");
    row.id = `${id}`;
    row.innerHTML = `
        <td>${name}</td>
        <td data-total=${price} data-price=${price}>${parseFloat(price).toLocaleString('en-US')} ₫</td>
        <td><input type="number" min="1" class="form-control" value=1 onblur='updatePriceMedicine("${id}")'></td>
        <td><input type="number" min="1" class="form-control" value=1 onblur='updatePriceMedicine("${id}")'></td>
        <td class="d-flex justify-content-center"><button class="btn btn-danger" onclick="deleteMedicine('${id}');">Xoá</button></td>
    `;

    tbody.dataset.total = `${parseFloat(tbody.dataset.total) + parseFloat(row.children[1].dataset.total)}`;
    document.getElementById("total-medicines").value = `Tổng tiền thuốc: ${parseFloat(tbody.dataset.total).toLocaleString("en-US")} ₫`;

    tbody.appendChild(row);
    select.options[select.selectedIndex].disabled = true;
    select.selectedIndex = 0;
}

function deleteMedicine(id) {
    let tbody = document.getElementById("list-medicines");
    let medicine = document.getElementById(id);

    tbody.dataset.total = `${parseFloat(tbody.dataset.total) - parseFloat(medicine.children[1].dataset.total)}`;
    document.getElementById("total-medicines").value = `Tổng tiền thuốc: ${parseFloat(tbody.dataset.total).toLocaleString("en-US")} ₫`;

    let option = document.getElementById(id.replace("tr", "option"));
    option.disabled = false;
    tbody.removeChild(medicine);
}

function updatePriceMedicine(id) {
    let medicine = document.getElementById(id);
    let dosage = medicine.children[2].children[0].value;
    let day = medicine.children[3].children[0].value;
    let price = medicine.children[1].dataset.price;

    let tbody = document.getElementById("list-medicines");
    tbody.dataset.total = `${parseFloat(tbody.dataset.total) - parseFloat(medicine.children[1].dataset.total)}`;

    medicine.children[1].dataset.total = `${(price * dosage * day)}`;
    medicine.children[1].textContent = `${(price * dosage * day).toLocaleString('en-US')} ₫`;

    tbody.dataset.total = `${parseFloat(tbody.dataset.total) + parseFloat(medicine.children[1].dataset.total)}`;
    document.getElementById("total-medicines").value = `Tổng tiền thuốc: ${parseFloat(tbody.dataset.total).toLocaleString("en-US")} ₫`;
}


function confirmAppointment(id) {
    let tbody_services = document.getElementById("list-services").children;
    let tbody_medicines = document.getElementById("list-medicines").children;
    let services = [];
    let medicines = [];

    Array.from(tbody_services).forEach(tr => {
        if (tr.id !== "tr-default") {
            service = {
                "service_id": parseInt(tr.id.replace("tr-service-", "")),
                "price_service": parseFloat(tr.children[1].dataset.price),
                "appointment_schedule_id": parseInt(id)
            }
            services.push(service);
        }
    });

    Array.from(tbody_medicines).forEach(tr => {
        medicine = {
            "medicine_id": parseInt(tr.id.replace("tr-medicine-", "")),
            "appointment_schedule_id": parseInt(id),
            "price_medicine": parseFloat(tr.children[1].dataset.price),
            "quantity_day": parseInt(tr.children[3].children[0].value),
            "dosage": parseInt(tr.children[2].children[0].value)
        }
        medicines.push(medicine)
    });

    let doctorNote = document.getElementById("doctor-note").value;

    fetch(`/api/appointment_doctor/${id}`, {
        method: "POST",
        body: JSON.stringify({
            "services": services,
            "medicines": medicines,
            "note": {"note": doctorNote, "appointment_schedule_id": parseInt(id)}
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.log(data);
    })
}