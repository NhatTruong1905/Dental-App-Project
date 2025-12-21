

function showTime() {
    document.getElementById("text-info-time").classList.add("d-none");
    document.getElementById("list-time").classList.remove("d-none");   
}

function hiddenTime() {
    let textInfoTime = document.getElementById("text-info-time")
    if (textInfoTime.classList.contains("d-none"))
        textInfoTime.classList.remove("d-none");

    let listTime = document.getElementById("list-time");
    if (listTime.classList.contains("d-none") === false)
        listTime.classList.add("d-none");
}


function loadTime(select) {
    let date = document.getElementById("date").value;
    doctor_id = select.options[select.selectedIndex].id
    fetch(`/api/doctors/${doctor_id}/${date}/times`).then(res => res.json()).then(data => {
        Array.from(data["time"]).forEach(time => {
            let id = time.trim().replace(":", "-");
            let bt = document.getElementById(id);
            bt.style.backgroundColor = "gray";
            bt.style.color = "white";
            bt.style.borderColor = "white";
            bt.disabled = true;
        })
    });
}