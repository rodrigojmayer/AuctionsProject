

document.addEventListener('DOMContentLoaded', function(){


    // alert("Its working!")
    // document.getElementById("user-logged").onmouseover=function(){
    //     document.getElementById("myDropdownUser").classList.add('show');
    //     document.getElementById("myDropdownUser").classList.remove('hide');

    // };
    // document.getElementById("user-logged").onmouseout=function(){
    //     document.getElementById("myDropdownUser").classList.add('hide');
    //     document.getElementById("myDropdownUser").classList.remove('show');
    // };
// 
    // document.getElementsByName("enable-answer")[0].addEventListener("click", function() {
        // this.style.backgroundColor = "red";
        // alert("RED")
    // });

    // document.querySelectorAll(".enable-answer").addEventListener("click", function() {
        // this.style.backgroundColor = "red";
        // alert("RED")
    // });
})

function enable_answer(varr){
    // return false;
    // alert(varr)
    let answer_form = document.getElementById("answer-form-"+varr);
    let add, remove
    // console.log(answer_form.classList);
    if(answer_form.classList.contains("show")){
        add = 'hide'
        remove = 'show'
    }
    else{
        add = 'show'
        remove = 'hide'
    }

    document.querySelectorAll(".answer-forms").forEach(function(el) {
        el.classList.add('hide');
        el.classList.remove('show');
    });

    answer_form.classList.add(add);
    answer_form.classList.remove(remove);
    // document.getElementById("answer-input-"+varr).style.backgroundColor="red";
    console.log(varr)
    
    setTimeout(function(){ document.querySelector("#answer-input-"+varr).focus(); }, 50);
}
function enable_question(){
    let question_form = document.getElementById("question-form"); 
    if(question_form.classList.contains("show")){
        add = 'hide';
        remove = 'show';
    }
    else{
        add = 'show';
        remove = 'hide';
    }
    question_form.classList.add(add);
    question_form.classList.remove(remove);
    
    setTimeout(function(){ document.getElementById("question-input").focus(); }, 50);
}