

function loadDate(max) {
    let selectDate = document.getElementById("select-date");

    let today = new Date();
    let days = ["Chủ nhật", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"];

    for (let i = 0; i <= max; i++) {
        let d = new Date(today);
        d.setDate(today.getDate() + i);

        let day = String(d.getDate()).padStart(2, "0");
        let month = String(d.getMonth() + 1).padStart(2, "0");
        let year = d.getFullYear();

        let option = document.createElement("option");
        option.value = `${year}-${month}-${day}`;
        option.textContent = `${days[d.getDay()]}, ngày ${day}-${month}-${year}`;

        selectDate.appendChild(option);
    }
}
