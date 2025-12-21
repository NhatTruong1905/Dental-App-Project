

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
    doctor_id = select.options[select.selectedIndex]
    fetch(`/api/doctors/%${doctor_id}/${date}/times`).then(res => res.json()).then(data => {
        console.log(data);
    });
}