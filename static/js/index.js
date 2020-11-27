const form = document.getElementById('form');
const emp_id = document.getElementById('id_employee_id');
const takeQuiz = document.getElementsByClassName("show-form")[0];

takeQuiz.onclick = () => {
    if(sessionStorage.length !== 0) {
        sessionStorage.removeItem('user_name');
        sessionStorage.removeItem('test_code');
    }
}


form.onsubmit = (e) => {
    e.preventDefault();
    const FD = new FormData(e.target);
    saveCustomer(FD);
}

    
emp_id.onchange = (e) => {
    let elm = e.target.value
    if(elm.length > 0){
        getCustomer(elm);
    }
}


function getCustomer(args) {
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let responseJsonObj = JSON.parse(this.responseText);
            let user_info = responseJsonObj.user_info;
            let test_code = responseJsonObj.test_code;

            if(user_info){
                let user_name = responseJsonObj.user_info.employee_id;
                sessionStorage.setItem("user_name", user_name);
                sessionStorage.setItem("test_code", test_code); 
                buildTable(user_info, user_name, test_code)
            }
        }
    }
    xmlhttp.open("GET", `/quizapp/create_customer?employee_id=${args}`, true);
    xmlhttp.send();
}

function buildTable(data, uname, tcode){
    var table = document.getElementById('modal-content')
    table.innerHTML = `<div class="modal-header"><h5 class="modal-title">Customer Info</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span></button></div><div class="modal-body pt-0">
        <table class="table table-bordered mt-1">
        <tr><th colspan="2" style="background-color: #0c499c;color: white">Customer Info</th></tr>
        <tr><th>Employee ID</th><td>${ data.employee_id }</td></tr>
        <tr><th>Employee Name</th><td>${ data.name }</td></tr>
        <tr><th>Gender</th><td>${ data.gender }</td></tr>
        <tr><th>Age</th><td>${ data.age }</td></tr>
        <tr><th>Location</th><td>${ data.location }</td></tr>
        <tr><th colspan="2" style="text-align:right">
        <p class="mb-0">Your data is already with us, still you want to continue
        <span><a id="quiz" onclick="test()" href="#"><br>Please proceed...&raquo;</a></span></p></th></tr></tr></table></div>`;
        //<span><a href="/quizapp/skin_quiz/" id="quiz">
}

function saveCustomer(formData) {
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let responseJsonObj = JSON.parse(this.responseText);
            let user_name = responseJsonObj.user_name;
            let test_code = responseJsonObj.test_code;
            sessionStorage.setItem("user_name", user_name);
            sessionStorage.setItem("test_code", test_code); 
            location.href = `/quizapp/skin_quiz/`;
            //location.href = `/quizapp/skin_quiz/${user_name}/${test_code}/`;
        }
    }
    xmlhttp.open("POST", "/quizapp/create_customer/", true);
    xmlhttp.send(formData);
}


/*
$("#quiz").click(function(){
    console.log('ok')
});
*/

function test(){
    let elm_clone = $(".card")
    //$('#modal-quiz').show()
    //$('#modal-quiz .modal-content').html(data.html_data);

    $(".container").html(elm_clone.clone());
}


