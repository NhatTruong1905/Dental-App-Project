function loadDoctor(date) {
    if (!date) return;

    fetch(`/api/doctors/check-date?date=${date}`, {
    }).then(res => res.json()).then(data => {
        let doctorSelect = document.getElementById("doctor-select")
        doctorSelect.innerHTML = ''

        let option = document.createElement('option')
        if (data.length > 0) {
            data.forEach(d => {
                option.value = d.id
                option.text = `${d.name}`
                doctorSelect.appendChild(option)
            })
        } else {
            option.text = `Ngày ${date} không có bác sĩ trống lịch hoặc rảnh`
            doctorSelect.appendChild(option)
        }
    })
}