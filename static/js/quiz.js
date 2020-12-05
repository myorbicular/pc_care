let quiz_type = '{{ quiz_type }}';
let user_name = sessionStorage.getItem("user_name");
let test_code = sessionStorage.getItem("test_code");
document.querySelector("span.name").innerHTML = user_name;
let question_count = 0;
let preBtn = document.getElementById('btn-previous');
let nextBtn = document.getElementById('btn-next');
let question_elm = document.getElementById("question");
let option_table = document.getElementById("option_table");
let ques_count = document.getElementById("ques_count");
let watr_intake = document.getElementById('watr-intake');
let water_content = document.getElementById('water-content');
let note = document.getElementById('note');
let e1_value, e2_value, e3_value, e4_value, water_val;
let questions = [];
ans_data = [];
water_msg = ['Hydrated', 'Dehydrated', 'Slightly Dehydrated']

////////////////////////testing/////////////
let quiz1 = (callback) => {
    var url = "/quizapp/quiz1/";
    //var params = `user_name=${user_name}&test_code=${test_code}`;
    //let json_params = JSON.stringify(params);

    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let responseJsonObj = JSON.parse(this.responseText);
            callback(responseJsonObj);
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send(null);
}
////////////////////////testing/////////////

window.onload = () => {
    quiz1((response)=>{
        //questions.push(response)
        questions = response ;
        
    });

    setTimeout(()=>{
        show(question_count);
    }, 600)
};

let previous = () => {
    question_count--;
    show(question_count);  
    
    let option = document.querySelectorAll("td.option");
    let ans_option_elm = document.getElementById(ans_data[question_count]);

    if (ans_option_elm) {
        ans_option_elm.classList.add("active");
    }
}

let next = () => {
    let retrieve_ans = document.querySelector("td.option.active");
    if(retrieve_ans){
        ans_data[question_count] = retrieve_ans.id;
    }else{
        ans_data[question_count] = 0;
    }
    // if the question is last then redirect to final page
    if (question_count === questions.length - 1) {
        nextBtn.classList.add('invisible');
        //SaveTest();
        SaveAns(ans_data);
        //WaterIntake();
    } else {
        question_count++;
        show(question_count);
    }
}

let show = (count) => {
    water_content.classList.add('d-none');
    note.classList.add('d-none');
    nextBtn.classList.add('invisible');
    if (question_count <= 0) {
        preBtn.classList.add('invisible');
    } else {
        preBtn.classList.remove('invisible');
    }

    ques_count.innerHTML = `Question ${count + 1} of ${questions.length}`;
    question_elm.innerHTML = `Q${count + 1}.${questions[count].name}`;
    let choice_data = questions[count].choices;

    if (questions[count].question_code == 107) {
        note.classList.remove('d-none');
        note.innerHTML = "Note: As per international standards 1ltr = 4.16 glasses"
        option_table.innerHTML = choice_data.map(choice => `<tr>
                            <td class='pt-0 pb-0' id='td1-${choice.id}'>${choice.name}</td>
                            <td width='20%' class='p-0'><input type='text' class='form-control formtest' id='${choice.id}'></td>
                            </tr>`).join("");
        let water_ltrs = document.querySelector("tr:nth-child(3) td:first-child")
        water_ltrs.insertAdjacentHTML("beforeend", '&nbsp;<input type="text" style="width: 50px;margin-left: 30px;" id="water-calc"> in ltrs');
        watercontent();
    } else {
        option_table.innerHTML = choice_data.map(choice => `<tr><td class='option' id='${choice.id}'>${choice.name}</td></tr>`).join("");
        toggleActive();
    }
} 

let watercontent = () => {
    let elm1 = watr_intake.elements[0];
    let elm2 = watr_intake.elements[1];
    let elm3 = watr_intake.elements[3];
    let elm4 = watr_intake.elements[4];
    let elm5 = watr_intake.elements[5];
    let elm6 = watr_intake.elements[6];

    elm4.readOnly = true;
    elm5.readOnly = true;
    elm6.readOnly = true;
    let water_info;

    let water_input = document.getElementById('water-calc');

    water_input.onchange = (e) => {
        let ltrs = e.target.value
        elm3.value = parseFloat(ltrs * 4.16).toFixed(1); 
        water_val = ltrs;
    }

    if(e1_value){
        elm1.value = e1_value;
        elm2.value = e2_value;
        elm3.value = e3_value;
        elm4.value = e4_value;
        water_input.value = water_val;
        water_input.focus();
        
        setTimeout(()=> {
            elm3.focus();
        }, 200);
    }

    watr_intake.addEventListener("change", water_calc);    
    water_input.addEventListener("focusout", water_calc);    
    //watr_intake.onchange = () => { 
    
    function water_calc(){
        //console.log(e.path[0])
        elm3.focusout = () => {
            e1_value = elm1.value;
            e2_value = elm2.value;
            e3_value = elm3.value;
            e4_value = elm4.value;
        }
    
        elm4_value = ((elm1.value * 2.2 * 2 / 3 * 30 / 240) + (12 * 30 * elm2.value / 30 / 240));
        elm5_value = (elm4_value - elm3.value);
        elm6_value = (elm5_value / elm4_value * 100);
        elm4.value = parseFloat(elm4_value).toFixed(1);
        elm5.value = parseFloat(elm5_value).toFixed(1);
        elm6.value = parseFloat(elm6_value).toFixed(1);
                        
        if (elm1.value >= 0 && elm2.value >= 0 && elm3.value) {
            //watr_intake.classList.remove('d-none');
            note.classList.remove('d-none');
            nextBtn.classList.remove('invisible')
            let msg = parseFloat(elm6_value);
            if(msg <= 0){
                water_info = water_msg[0]; //'Hydrated'
            } else if(msg > 25){
                water_info = water_msg[1]; //'Dehydrated'
                water_info = 'Dehydrated'
            } else {
                water_info = water_msg[2]; // 'Slightly Dehydrated'
            };
        } else {
            water_info = '' 
            nextBtn.classList.add('invisible')
        }
        water_content.classList.remove('d-none')
        water_content.innerHTML = water_info;
    };
}

let toggleActive = () => {
    let option = document.querySelectorAll("td.option");
    for (let i = 0; i < option.length; i++) {
        option[i].onclick = () => {
            for (let i = 0; i < option.length; i++) {
                if (option[i].classList.contains("active")) {
                    option[i].classList.remove("active");
                }
            }
            option[i].classList.add("active");
            nextBtn.classList.remove('invisible')
        };
    }
}


let SaveTest = () => {
    let url = "/quizapp/skin_test/";
    let params = {code:test_code, user_name:user_name};
    let json_params = JSON.stringify(params);

    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let responseJsonObj = JSON.parse(this.responseText);
        }
    }
    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    xmlhttp.send(json_params);
}

////////////////////////sae data/////////////
//let SaveAns = (obj) => {
let SaveAns = (obj) => {
    let ans_json = JSON.stringify(obj);
    //let primary_concern = '{{ primary }}';
    //let skin_concerns = JSON.parse("{{category_choice|escapejs}}");
    let params = {user_choice:ans_json, user_name:user_name, test_code:test_code};
    $.ajax({
        url: '/quizapp/quizanswers/',
        type: 'POST',
        contentType: 'application/json',
        data: params,
        dataType: 'json',
        success: (response)=>{
            if (response) {
                if(quiz_type ===  'skin'){
                    //WaterIntake();
                    location.href = `/quizapp/skin_concerns/${user_name}/${test_code}/`;
                } else {
                    location.href = `/quizapp/products/${user_name}/${test_code}/`;
                }
            }
        }
    })
}

////////////////////////save water information/////////////
let WaterIntake = () => {
    let params = {
        user_name : user_name,
        weight : e1_value,
        physical_activity : e2_value,
        water_intake : e3_value,
        status : water_content.textContent,
        test_code : test_code,
    };

    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let responseJsonObj = JSON.parse(this.responseText);
            questions = responseJsonObj;
        }
    }
    xmlhttp.open("POST", "/quizapp/water_info/", true);
    xmlhttp.send(params);
}