

function deletePatient(id) {
    if (confirm("Bạn có chắc muốn xoá hồ sơ này không?")) {
         fetch(`/api/patients/${id}`, { method: "DELETE" })
        .then(res => res.json())
        .then(data => {
            console.info(data)
            let patient = document.getElementById(`patient${id}`)
            patient.style.display = "none"
        })
    }
}

function getPatients() {
    fetch("/api/patients").then(res => res.json()).then(data => {
        let select = document.getElementById("select-patient");
        for (patient of data) {
            let option = new Option(patient['name']);
            option.id = patient['id'];
            select.appendChild(option);
        }
    });
}

