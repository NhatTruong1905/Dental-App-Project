function loadAppointmentSuccess(date) {
    fetch(`/api/appointment_schedule/${date}`).then(res => res.json()).then(data => {
        let appointmentSelect = document.getElementById("select-appointment")


        if (data.length > 0) {
            let selected = document.getElementById("selected-appointment");
            selected.textContent = `-- Chọn lịch khám --`;
            for (let a of data) {
                let option = document.createElement('option')
                option.textContent = `Lịch khám lúc ${a["start_time"]} - ${a["patient_name"]} - ${a["patient_phone"]}`
                option.value = a["id"]
                appointmentSelect.appendChild(option)
            }

        } 
        else {
            let selected = document.getElementById("selected-appointment");
            selected.textContent = `-- Không có lịch khả dụng --`;
            selected.selected = true;
        }
    })
}

function reloadInvoice() {
    let appointmentSelect = document.getElementById("select-appointment");
    Array.from(appointmentSelect.options).forEach(option => {
        if (option.id != "selected-appointment")
            option.remove();
    })

    let tbody_services = document.getElementById("list-services");
    let tbody_medicines = document.getElementById("list-medicines");

    tbody_services.innerHTML = '';
    tbody_medicines.innerHTML = '';

    document.getElementById("total-services").dataset.totalservices = "0";
    document.getElementById("total-medicines").dataset.totalmedicines = "0";
    document.getElementById("total-vat").dataset.totalvat = "0";
    document.getElementById("total-result").dataset.totalresult = "0";

    document.getElementById("total-services").textContent = "0 VNĐ";
    document.getElementById("total-medicines").textContent = "0 VNĐ";
    document.getElementById("total-vat").textContent = "0 VNĐ";
    document.getElementById("total-result").textContent = "0 VNĐ";
}

function reloadListAppointments() {
    let tbody_services = document.getElementById("list-services");
    let tbody_medicines = document.getElementById("list-medicines");
    tbody_services.innerHTML = "";
    tbody_medicines.innerHTML = "";
}

function calculateTotalServices() {

    let id = document.getElementById("select-appointment").value
    let totalServices = document.getElementById("total-services")


    return fetch(`/api/appointment_schedule/${id}/total_services`).then(res => res.json()).then(data => {
        if (data["ok"]) {
            Array.from(data["service_list"]).forEach(s => {
                let tbody = document.getElementById("list-services");
                let row = document.createElement("tr");
                row.innerHTML = `
                    <td>${s["name"]} </td>
                    <td>${parseFloat(s["price"]).toLocaleString('en-US')} ₫</td>
                `;
                tbody.appendChild(row);
            })
            totalServices.textContent = data["total_services"].toLocaleString('vi-VN') + " VNĐ"
            totalServices.dataset.totalservices = data["total_services"];
        }
        else {
            console.log(data["error"]);
        }
    })
}

function calculateTotalMedicines() {
    let id = document.getElementById("select-appointment").value
    let totalMedicines = document.getElementById("total-medicines")


    return fetch(`/api/appointment_schedule/${id}/total_medicines`).then(res => res.json()).then(data => {
        if (data["ok"]) {
            Array.from(data["medicine_list"]).forEach(m => {
                let tbody = document.getElementById("list-medicines");
                let row = document.createElement("tr");
                row.innerHTML = `
                    <td>${m["medicine_name"]} </td>
                    <td>${parseFloat(m["price_medicine"]).toLocaleString('en-US')} ₫</td>
                    <td>${m["dosage"]}</td>
                    <td>${m["quantity_day"]}</td>
                `;
                tbody.appendChild(row);
            })
            totalMedicines.textContent = data["total_medicines"].toLocaleString('vi-VN') + " VNĐ"
            totalMedicines.dataset.totalmedicines = data["total_medicines"];
        }
        else {
            console.log(data["error"]);
        }
    })
}

function calculateTotalVatAndResult() {
    let totalSerivcesStr = document.getElementById("total-services").dataset.totalservices
    let totalMedicinesStr = document.getElementById("total-medicines").dataset.totalmedicines

    let services = parseFloat(totalSerivcesStr)
    let medicines = parseFloat(totalMedicinesStr)

    let totalVAT = (services + medicines) * 0.1
    let totalResult = services + medicines + totalVAT

    let totalVatFinal = document.getElementById("total-vat")
    let totalResultFinal = document.getElementById("total-result")
    totalVatFinal.textContent = totalVAT.toLocaleString("vi-VN") + " VNĐ"
    totalResultFinal.textContent = totalResult.toLocaleString("vi-VN") + " VNĐ"

    totalVatFinal.dataset.totalvat = `${(services + medicines) * 0.1}`;
    totalResultFinal.dataset.totalresult = `${services + medicines + totalVAT}`;
}

async function finalResult() {
    await calculateTotalServices()
    await calculateTotalMedicines()
    calculateTotalVatAndResult()
}


function saveInvoice() {
    let total_service = parseFloat(document.getElementById("total-services").dataset.totalservices);
    let total_medicine = parseFloat(document.getElementById("total-medicines").dataset.totalmedicines);
    let vat = parseFloat(document.getElementById("total-vat").dataset.totalvat)
    let result = parseFloat(document.getElementById("total-result").dataset.totalresult)

    let selectAppointment = document.getElementById("select-appointment");
    let id_appointment_schedule = parseInt(selectAppointment.value)

    if (!id_appointment_schedule || selectAppointment.selectedIndex === 0) {
        let alertBox = document.getElementById("alert-appointment");
        alertBox.textContent = "Vui lòng chọn lịch khám trước khi lưu!";
        alertBox.classList.remove("d-none");
        alertBox.classList.add("alert-danger");
        return;
    }

    fetch(`/api/appointment_schedule/invoice`, {
        method: "POST",
        body: JSON.stringify({
            'id': id_appointment_schedule,
            'total_service': total_service,
            'total_medicine': total_medicine,
            'vat': vat,
            'total_invoice': result
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let alert = document.getElementById("alert-appointment")

        if (data["ok"]) {
            alert.textContent = "Lưu hóa đơn thành công"
            alert.classList.replace("alert-danger", "alert-success");
            alert.classList.remove("d-none");
            alert.classList.remove("alert-error")
            setTimeout(() => {
                window.location.href = "/";
            }, 1500)
        } else {
            alert.textContent = "Lỗi: " + (data["error"] || "Lưu không thành công");
            alert.classList.replace("alert-success", "alert-danger");
            alert.classList.remove("d-none");
        }
    }).catch(err => {
        let alert = document.getElementById("alert-appointment");
        alert.textContent = "Không thể kết nối đến máy chủ!";
        alert.classList.remove("d-none");
        console.error("error:", err);
    })
}



