function loadAppointmentSuccess(date) {
    fetch(`/api/appointment_schedule/${date}`).then(res => res.json()).then(data => {
        let appointmentSelect = document.getElementById("select-appointment")
        appointmentSelect.innerHTML = ""

        if (data.length > 0) {
            for (let a of data) {
                let option = document.createElement('option')
                option.textContent = `Lịch khám lúc ${a["start_time"]} - ${a["patient_name"]} - ${a["patient_phone"]}`
                option.value = a["id"]
                appointmentSelect.appendChild(option)
            }
            document.getElementById("total-services").textContent = "0 VNĐ";
            document.getElementById("total-medicines").textContent = "0 VNĐ";
            document.getElementById("total-vat").textContent = "0 VNĐ";
            document.getElementById("total-result").textContent = "0 VNĐ";
        } else {
            let option = document.createElement('option')
            option.textContent = "-- Không có lịch khả dụng --"
            appointmentSelect.appendChild(option)
            document.getElementById("total-services").textContent = "0 VNĐ";
            document.getElementById("total-medicines").textContent = "0 VNĐ";
            document.getElementById("total-vat").textContent = "0 VNĐ";
            document.getElementById("total-result").textContent = "0 VNĐ";
        }
    })
}

function calculateTotalServices() {
    let id = document.getElementById("select-appointment").value
    let totalServices = document.getElementById("total-services")
    let servicesAppointment = document.getElementById("select-services-list")

    totalServices.innerHTML = ""
    servicesAppointment.innerHTML = ""

    return fetch(`/api/appointment_schedule/${id}/total_services`).then(res => res.json()).then(data => {
        if (data["total_services"] === 0 || !data["total_services"] || data["service_list"].length === 0) {
            totalServices.textContent = "Không có giá dịch vụ"
            let option = document.createElement('option')
            option.textContent = "Không có dịch vụ khả dụng"
            servicesAppointment.appendChild(option)
        } else {
            totalServices.textContent = data["total_services"].toLocaleString('vi-VN') + " VNĐ"
            for (let s of data['service_list']) {
                let option = document.createElement('option')
                option.textContent = s
                servicesAppointment.appendChild(option)
            }
        }
    })
}

function calculateTotalMedicines() {
    let id = document.getElementById("select-appointment").value
    let totalMedicines = document.getElementById("total-medicines")
    let medicinesAppointment = document.getElementById("select-medicines-list")

    totalMedicines.innerHTML = ""
    medicinesAppointment.innerHTML = ""


    return fetch(`/api/appointment_schedule/${id}/total_medicines`).then(res => res.json()).then(data => {
        if (data["total_medicines"] === 0 || !data["total_medicines"] || data['total_medicines'] === 0) {
            totalMedicines.textContent = "Không có giá thuốc"
            let option = document.createElement('option')
            option.textContent = "Không có dịch vụ khả dụng"
            medicinesAppointment.appendChild(option)
        } else {
            totalMedicines.textContent = data["total_medicines"].toLocaleString('vi-VN') + " VNĐ"
            for (let m of data["medicine_list"]) {
                let option = document.createElement('option')
                option.textContent = `${m["medicine_name"]} - Số lượng: ${m["quantity_day"]} - Liều lượng: ${m["dosage"]}`
                medicinesAppointment.appendChild(option)
            }
        }
    })
}

function calculateTotalVatAndResult() {
    let totalSerivcesStr = document.getElementById("total-services").textContent.replace(/[^\d]/g, '') || 0
    let totalMedicinesStr = document.getElementById("total-medicines").textContent.replace(/[^\d]/g, '') || 0

    let services = parseFloat(totalSerivcesStr)
    let medicines = parseFloat(totalMedicinesStr)

    let totalVAT = (services + medicines) * 0.1
    let totalResult = services + medicines + totalVAT

    let totalVatFinal = document.getElementById("total-vat")
    let totalResultFinal = document.getElementById("total-result")
    totalVatFinal.textContent = totalVAT.toLocaleString("vi-VN") + " VNĐ"
    totalResultFinal.textContent = totalResult.toLocaleString("vi-VN") + " VNĐ"
}

async function finalResult() {
    await calculateTotalServices()
    await calculateTotalMedicines()

    calculateTotalVatAndResult()
}


function saveInvoice() {
    let total_service = parseFloat(document.getElementById("total-services").textContent.replace(/[^\d]/g, '')) || 0
    let total_medicine = parseFloat(document.getElementById("total-medicines").textContent.replace(/[^\d]/g, '')) || 0
    let vat = parseFloat(document.getElementById("total-vat").textContent.replace(/[^\d]/g, '')) || 0
    let result = parseFloat(document.getElementById("total-result").textContent.replace(/[^\d]/g, '')) || 0

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
            }, 1500);
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



