const form = document.getElementById('form');
const emp_id = document.getElementById('id_employee_id');
const takeQuiz = document.getElementsByClassName("show-form")[0];

takeQuiz.onclick = () => {
    if(sessionStorage.length !== 0) {
        sessionStorage.removeItem("customer_pk");           
        sessionStorage.removeItem("skinTest_pk");         
        sessionStorage.removeItem('user_name');        
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
    let url = `/quizapp/customers?employee_id=${args}`;
    let xmlhttp = new XMLHttpRequest();
    //let url = `/quizapp/create_customer?employee_id=${args}`

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let resObj = JSON.parse(this.responseText)[0];
            //let test_data = responseJsonObj.map(x => `<p>${x}</p>`);

            if(resObj){
                sessionStorage.setItem("customer_pk", resObj.id);                
                sessionStorage.setItem("user_name", resObj.employee_id);                
                buildTable(resObj)
            }
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function buildTable(data){
    var table = document.getElementById('modal-content')
    table.innerHTML = `<div class="modal-header"><h5 class="modal-title">Customer Info</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span></button></div><div class="modal-body pt-0">
        <table class="table table-bordered mt-1">
        <tr><th colspan="2" style="background-color: #0c499c;color: white">Customer Info</th></tr>
        <tr><th>Employee ID</th><td>${data.employee_id}</td></tr>
        <tr><th>Employee Name</th><td>${data.name}</td></tr>
        <tr><th>Gender</th><td>${data.gender}</td></tr>
        <tr><th>Age</th><td>${data.age }</td></tr>
        <tr><th>Location</th><td>${data.location}</td></tr>
        <tr><th colspan="2" style="text-align:right">
        <p class="mb-0">Your data is already with us, still you want to continue
        <span><a id="quiz" href="#" onclick="SaveTest(${data.id})"><br>Please proceed...&raquo;</a></span></p></th></tr></tr></table></div>`;
        //<span><a href="/quizapp/skin_quiz/" id="quiz">
}

function saveCustomer(formData) {
    let url = "/quizapp/customers/";

    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 201) {
            let resObj = JSON.parse(this.responseText);
            sessionStorage.setItem("customer_pk", resObj.id);              
            sessionStorage.setItem("user_name", resObj.employee_id);
            SaveTest(resObj.id)
            //location.href = `/quizapp/skin_quiz/${user_name}/${test_code}/`;
        }
    }
    xmlhttp.open("POST", url, true);
    xmlhttp.send(formData);
}


let SaveTest = (customer) => {    
    let url = "/quizapp/skin_test/";    
    let json_params = JSON.stringify({customer:customer});

    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 201) {
            let resObj = JSON.parse(this.responseText);
            sessionStorage.setItem("skinTest_pk", resObj.id);
            location.href = `/quizapp/skin_quiz/`;
        }
    }
    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    xmlhttp.send(json_params);
}

/*
$("#quiz").click(function(){
    console.log('ok')
});


function test(){
    let elm_clone = $(".card")
    //$('#modal-quiz').show()
    //$('#modal-quiz .modal-content').html(data.html_data);

    $(".container").html(elm_clone.clone());
}

*/