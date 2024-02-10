loader(false);
document.addEventListener("DOMContentLoaded", function () {
  let loginform = document.getElementById("loginform");
  let alerttt = document.getElementById("alerttt");
  loginform.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(loginform);
    loader(true);
    fetch(loginform.getAttribute("action"), {
      method: loginform.getAttribute("method"),
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        loader(false);
        content = `
        <div class="container">
<div  class="alert alert-danger" role="alert">
 <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  ${data.msg}


</div>

</div>
        `;

        // console.log(data.msg);
        // console.log(data);
        let fullpath = document.getElementById("fullpath");

        if (data.msg) {
          loader(false);
          alerttt.innerHTML = content;
        } else if (data.smsg && fullpath.value == "/cart/") {
          hidemodal();
          loader(false);
          location.href = "/cart/";
        } else if (data.smsg) {
          hidemodal();
          loader(false);
          location.href = "/dashboard/";
        }
      });
  });
});
function loader(show = true) {
  if (show) {
    document.getElementById("loder").style.visibility = "visible";
  } else {
    document.getElementById("loder").style.visibility = "hidden";
  }
}
function hidemodal() {
  const modal = document.getElementById("LoginModale");
  modal.style.visibility = "hidden";
}
allertwi = document.getElementById("Alertwi");
if ((allertwi.style.display = "block")) {
  setInterval(function () {
    allertwi.style.display = "none";
  }, 5000);
}
