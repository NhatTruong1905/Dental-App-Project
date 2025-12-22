


function handleAppointment(time) {
    let patient = document.getElementById("select-patient");
    patient = patient.options[patient.selectedIndex];

    let service = document.getElementById("select-service");
    service = service.options[service.selectedIndex];

    let date = document.getElementById("date").value;

    let doctor = document.getElementById("doctor-select");
    doctor = doctor.options[doctor.selectedIndex]

    let alert = document.getElementById("alert-appointment");
    if (patient.id === "selected-patient" || service.id === "selected-service" || doctor.id === "selected-doctor") {
        alert.textContent = "Vui lòng nhập đủ tin!";
        alert.classList.remove("d-none");
        return;
    }

    fetch("/api/appointment_schedule", {
        method: "POST",
        body: JSON.stringify({
            "patient_id": patient.id,
            "service_id": service.id,
            "doctor_id": doctor.id,
            "start_time": `${date} ${time.textContent}:00`
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.log(data);
        if (data["ok"]) {
            let alertSuccess = document.getElementById("alert-appointment");
            if (alertSuccess) {
                alertSuccess.textContent = "Đặt lịch khám thành công!";
                alertSuccess.classList.remove("alert-error")
                alertSuccess.classList.remove("d-none")
                window.location.href = "/";
            }
            else {
                console.log("element not found");
            }
        }
        else {
            let alertError = document.getElementById("alert-appointment");
            if (alertError) {
                alertError.textContent = "Đặt lịch khám không thành công vui lòng thử lại sau!";
                alertError.classList.add("alert-error")
                alertError.classList.remove("d-none")
                window.location.href = "/";
            }
            else {
                console.log("element not found");
            }
        }
    })
    

    alert.classList.add("d-none");
    console.log("ok");
}