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
    totalServices.innerHTML = ""

    return fetch(`/api/appointment_schedule/${id}/total_services`).then(res => res.json()).then(data => {
        if (data["total_services"] === 0 || !data["total_services"]) {
            totalServices.textContent = "Không có giá dịch vụ"
        } else {
            totalServices.textContent = data["total_services"].toLocaleString('vi-VN') + " VNĐ"
        }
    })
}

function calculateTotalMedicines() {
    let id = document.getElementById("select-appointment").value
    let totalMedicines = document.getElementById("total-medicines")
    totalMedicines.innerHTML = ""

    return fetch(`/api/appointment_schedule/${id}/total_medicines`).then(res => res.json()).then(data => {
        if (data["total_medicines"] === 0 || !data["total_medicines"]) {
            totalMedicines.textContent = "Không có giá thuốc"
        } else {
            totalMedicines.textContent = data["total_medicines"].toLocaleString('vi-VN') + " VNĐ"
        }
    })
}

function calculateTotalVatAndResult() {
    let totalSerivcesStr = document.getElementById("total-services").textContent.replace(/[^\d]/g, '')
    let totalMedicinesStr = document.getElementById("total-medicines").textContent.replace(/[^\d]/g, '')

    let services = parseFloat(totalSerivcesStr)
    let medicines = parseFloat(totalMedicinesStr)

    let totalVAT = (services + medicines) * 0.1
    let totalResult = services + medicines + totalVAT

    let totalVatFinal = document.getElementById("total-vat")
    let totalResultFinal = document.getElementById("total-result")
    totalVatFinal.textContent = totalVAT.toLocaleString("vi-VN") + " VNĐ"
    totalResultFinal.textContent = totalResult.toLocaleString("vi-VN") + " VNĐ"
}

async function finalTotal() {
    await calculateTotalServices()
    await calculateTotalMedicines()

    calculateTotalVatAndResult()
}




