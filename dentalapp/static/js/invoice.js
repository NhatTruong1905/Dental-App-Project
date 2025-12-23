function loadAppointmentSuccess(date) {
    fetch(`/api/appointment_schedule/${date}`).then(res => res.json()).then(data => {
        let appointmentSelect = document.getElementById("select-appointment")
        appointmentSelect.innerHTML = ""

        if (data.length > 0) {
            for (let a of data) {
                let option = document.createElement('option')
                option.textContent = `Lịch khám ${a["start_time"]}`
                option.value = a["id"]
                option.dataset.patientName = a["patient_name"]
                option.dataset.patientPhone = a["patient_phone"]
                // optionPatient.textContent = `${a["patient_name"]} - ${a["patient_phone"]}`
                appointmentSelect.appendChild(option)
            }
        } else {
            let option = document.createElement('option')
            let patient = document.getElementById("patient-info")
            option.textContent = "-- Không có lịch khả dụng --"
            patient.textContent = "Không có bệnh nhân"
            appointmentSelect.appendChild(option)
        }
    })
}

function getPatientFromAppointment() {
    let appointmentSelect = document.getElementById("select-appointment")
    let patient = document.getElementById("patient-info")

    patient.addEventListener('appointmentSelect', function () {
        let selectApp = this.value
        let options = appointmentSelect.options

        selectedPatient.innerHTML = ""

        for (let i = 0; i < options.length; i++) {
            if (options[i].value === selectApp) {
                selectedPatient.value = options[i].id
                break
            }
        }
    })
}

// function loadPatients(phone) {
//     if (phone.length < 4) return
//     date = document.getElementById("selected-appointment")
//
//     fetch(`/api/patients/${date}/${phone}`, {}).then(res => res.json()).then(data => {
//         let patientList = document.getElementById('patient-list')
//
//         patientList.innerHTML = ""
//
//         if (data.length > 0) {
//             for (let patient of data) {
//                 let option = document.createElement('option')
//                 option.value = `${patient['name']} - ${patient['phone']}`
//                 option.dataset.id = patient['id']
//                 patientList.appendChild(option)
//             }
//
//         } else {
//             console.info("Không tải được danh sách bệnh nhân")
//         }
//     }).catch(err => console.error("Lỗi API", err))
// }
//
// function getPhone() {
//     let phone = document.getElementById('patient-search')
//     let patientList = document.getElementById('patient-list')
//     let input = document.getElementById('patient-id-hidden')
//
//     phone.addEventListener('input', function () {
//         let inputValue = this.value
//         let options = patientList.options
//
//         input.innerHTML = ""
//
//         for (let i = 0; i < options.length; i++) {
//             if (options[i].value === inputValue) {
//                 input.value = options[i].dataset.id
//                 break
//             }
//         }
//     })
// }



