


function handleAppointment(time) {
    let patient = document.getElementById("select-patient");
    patient = patient.options[patient.selectedIndex];

    let service = document.getElementById("select-service");
    service = service.options[service.selectedIndex];

    let date = document.getElementById("select-date");
    date = date.options[date.selectedIndex].value;
    console.log(date);

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
        window.location.href = data["ok"] ? "/?success=1" : "/?success=0";
    })
    

    alert.classList.add("d-none");
    console.log("ok");
}


function deleteAppointment(id) {
    if (confirm("Bạn có chắc chắn xoá lịch khám này không?") === false)
        return;

    fetch(`/api/appointment_schedule/${id}`, {
        method: "DELETE"
    }).then(res => res.json()).then(data => {
        console.log(data);
        if (data["ok"]) {
            let appointment = document.getElementById(`appointment${id}`);
            appointment.style.display = "none";
        }
        else
            console.log("Can not delete appointment");
    })
}