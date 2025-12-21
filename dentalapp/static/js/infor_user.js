function handleUploadAvatar(object) {
    let file = object.files[0];
    let avatar = document.getElementById("render_avatar");
    avatar.src = URL.createObjectURL(file);
}

function updateInforUser() {
    let id = document.getElementById("user_id").value;
    let name = document.getElementById("name").value;
    let phone = document.getElementById("phone").value;
    let avatar = document.getElementById("avatar").files[0];

    let regex = /^(01|02|03|04|05|06|07|08|09)\d{8}$/;
    if (regex.test(phone) === false) {
        let warning = document.getElementById("warning");
        warning.textContent = "Số điện thoại không hợp lệ!";
        warning.classList.remove("d-none");
        return;
    }

    let data = new FormData();
    data.append("name", name);
    data.append("phone", phone);
    data.append("avatar", avatar);

    fetch(`/api/users/${id}`, {
        method: "PUT",
        body: data
    }).then(res => res.json()).then(data => {
        console.log(data);
        window.location.href = "/user";
    });
}
