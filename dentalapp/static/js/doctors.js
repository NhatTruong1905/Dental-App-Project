function loadDoctor(date) {
    if (!date) return;

    fetch(`/api/doctors/check-date?date=${date}`, {
    }).then(res => res.json()).then(data => {
        let doctorSelect = document.getElementById("doctor-select")

        if (data.length > 0) {
            let selected = document.getElementById("selected");
            selected.textContent = "-- Chọn bác sĩ --";
            for (doctor of data) {
                let option = document.createElement('option')
                option.textContent = doctor["name"];
                option.id = doctor["id"];
                doctorSelect.appendChild(option);
            }
        } else {
            let selected = document.getElementById("selected");
            selected.textContent = `-- Ngày ${date} không có bác sĩ hoặc bận --`;
            let doctorSelect = document.getElementById("doctor-select");
        }
    });
}

function reloadDoctor() {
    let doctorSelect = document.getElementById("doctor-select")
    Array.from(doctorSelect.options).forEach(option => {
        if (option.id !== "selected")
            option.remove();
    });
}