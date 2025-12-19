

function deletePatient(id) {
    if (confirm("Bạn có chắc muốn xoá hồ sơ này không?")) {
         fetch(`/api/patients/${id}`, { method: "DELETE" })
        .then(res => res.json())
        .then(data => {
            console.info(data)
            let patient = document.getElementById(`patient${id}`)
            patient.style.display = "none"
        })
        .catch(err => console.error(err))
    }
}
