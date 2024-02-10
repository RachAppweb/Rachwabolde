const url = new URLSearchParams(window.location.search);

let search = url.get("search");
let nofound = document.getElementById("nosearch");
if (nofound) {
  if (search) {
    nofound.innerHTML = `Sorry, No result Found For -- ${search} --`;
  }
}

let urlparam = new URLSearchParams(window.location.search);
let resetparam = urlparam.get("reset");

$(document).ready(function () {
  if (resetparam == "success") {
    $("#LoginModale").modal("show");
    $("#alerttt").html(`    <div class="container">
              <div  class="alert alert-info" role="alert">
               <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> 
               <i class="fas fa-info"></i> 
                المرجو مراجعة بريدكم الإلكتروني وإتباع الخطوات لإعادة تعيين كلمة السر الخاصة بكم
              </div>
              </div>`);
  } else if (resetparam == "error") {
    $("#LoginModale").modal("show");
    $("#alerttt").html(`    <div class="container">
              <div  class="alert alert-danger" role="alert">
               <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> 
                
                يبدو أن رابط الإستعادة المرسل إليكم قد إنتهت صلاحيته إضغط على هل نسيت كلمة السر وحاول مرة اخرى
              </div>
              </div>`);
  } else if (resetparam == "newpass") {
    $("#LoginModale").modal("show");
    $("#alerttt").html(`    <div class="container">
              <div  class="alert alert-success" role="alert">
               <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> 
             <i class="fas fa-check"></i> 
             تمت إستعادة كلمة السر بنجاح
              </div>
              </div>`);
  } else if (resetparam == "youlogin") {
    $("#LoginModale").modal("show");
    $("#alerttt").html(`    <div class="container">
              <div  class="alert alert-warning" role="alert">
               <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> 
             <i class="fas fa-info"></i> 
             المرجو تسجيل الدخول أو إنشاء حساب إذا لم يكن لديكم
              </div>
              </div>`);
  }
});
