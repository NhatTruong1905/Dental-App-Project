

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

function resetTime() {
    document.querySelectorAll(".time-btn").forEach(btn => {
        btn.disabled = false;
            btn.style.backgroundColor = "white";
            btn.style.color = "blue";
            btn.style.borderColor = "blue";         
    });
}


function loadTime(select) {
    let date = document.getElementById("date").value;
    let doctor_id = select.options[select.selectedIndex].id;
    resetTime();
    fetch(`/api/doctors/${doctor_id}/${date}/times`)
        .then(res => res.json())
        .then(data => {
            if (!data["time"])
                return;
            Array.from(data["time"]).forEach(time => {
                console.log(time);
                let id = time.trim().replace(":", "-");
                let btn = document.getElementById(id);
                btn.style.backgroundColor = "gray";
                btn.style.color = "white";
                btn.style.borderColor = "gray";
                btn.disabled = true;
            });
        });
}

let pre_btn = null;
let btnClick = null;
Array.from(document.getElementsByClassName("time-btn")).forEach(btn => {
    btn.addEventListener("click", () => {
        if (pre_btn !== null) {
            pre_btn.style.backgroundColor = "white";
            pre_btn.style.color = "blue";
        }
        btn.style.backgroundColor = "blue";
        btn.style.color = "white";
        pre_btn = btn;
        btnClick = btn;
    });
});