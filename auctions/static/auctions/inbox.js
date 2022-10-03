

document.addEventListener('DOMContentLoaded', function(){


    charge_categories();
    
    
    // document.querySelector("#id_create_listing > form > div > input.btn.btn-primary").addEventListener("click", function() {
    //     this.style.backgroundColor = "red";
    //     alert("RED")
    // });

    let inputElement = document.getElementById("input");
    if(inputElement)
        inputElement.addEventListener("change", handleFiles, false);

    function handleFiles() {
        label_button = document.querySelector("#button_image p")
        
        label_button.classList.add('hide');
        label_button.classList.remove('show');
        let fileList = this.files; /* now you can work with the file list */
        // console.log(fileList)
        document.getElementById("image").files = fileList
        // console.log(fileList[0].name)

        // console.log(fileList[0].name)
        document.getElementById("glosaArchivos").innerText = fileList[0].name;
        img = document.getElementById("display-image");
        img.style.display = "block";
        img.src = URL.createObjectURL(fileList[0]);

        
    }
    
    let modal_alert = document.querySelector(".modal-alert");
    let accept = document.getElementById("accept");
    if(accept)
        accept.addEventListener("click", handleModal, false)

    function handleModal() {
        // alert("entrando al submit")
        modal_alert.classList.add('show');
        modal_alert.classList.remove('hide');

        let modal_subtitle = document.getElementById("modal_subtitle");
        let modal_text = document.getElementById("modal_text");
        let modal_back = document.getElementById("modal_back");
        let modal_save = document.getElementById("modal_save");
        
        let data_article = document.getElementById("data_article");
        let data_description = document.getElementById("data_description");
        let data_initial_price = document.getElementById("data_initial_price");
        let data_auction_category = document.getElementById("data_auction_category");
        let data_image = document.getElementById("image");
        let modal_answer_text = "", modal_answer_subtitle
        // data_article.value=1
        // data_description.value=1
        // data_initial_price.value=1
        // data_image.value=1

        
        if(!data_article.value){
            console.log("Article name missing")
            modal_answer_text += "- Name</br>"
        }
        if(!data_description.value){
            console.log("Description missing")
            modal_answer_text += " - Description</br>"
        }
        if(!data_initial_price.value){
            console.log("Price missing")
            modal_answer_text += " - Price</br>"
        }
        if(!data_auction_category.value){
            console.log("Category missing")
            modal_answer_text += " - Category</br>"
        }
        if(!data_image.value){
            console.log("Image missing")
            modal_answer_text += " - Image</br>"
        }

        if(modal_answer_text){
            modal_subtitle.innerHTML = "Missing data"
            modal_text.innerHTML = `You need to enter: </br> ${modal_answer_text}`
            rejected_modal()
        }
        else{

            const formData = new FormData();
            formData.append('name', data_article.value);
            formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
            // console.log(formData);
            fetch(`/check_auction/`, {
                method: 'POST',
                body:formData,
            })
            .then(response => response.json())
            .then(result => {
                console.log(result.auction_repeated)
                if(result.auction_repeated){
                    modal_subtitle.innerHTML = "Duplicate data"
                    modal_text.innerHTML = "There is already an active article with that name."
                    rejected_modal()
                }
                else{
                    modal_subtitle.innerHTML = "Post item"
                    modal_text.innerHTML = `Name: ${data_article.value}</br>
                                            Description: ${data_description.value}</br>
                                            Price: ${data_initial_price.value}</br>
                                            Category: ${data_auction_category.value}</br>
                                            Image: ${document.getElementById("glosaArchivos").textContent}</br>`
                    modal_save.classList.remove('hide');
                    modal_save.classList.add('show');
                    modal_save.onclick="";
                }

            })
            .catch((error) => {
                console.log(error)
            });
        }
        modal_back.addEventListener("click", function() {
            modal_alert.classList.add('hide');
            modal_alert.classList.remove('show');
        })
    
        function rejected_modal(){
            modal_save.classList.remove('show');
            modal_save.classList.add('hide');
        }
        // modal_text

        // console.log(data_article.value);
        // console.log(data_description.value);
        // console.log(data_initial_price.value);
        // console.log(data_auction_category.value);
        // console.log(data_image.value);

    };
    

    // const image_input = document.querySelector("#change_profile_picture");
    // image_input.addEventListener("change", function(e) {

    //     alert("holis")
    //     if (e.target.files) {
    //         let imageFile = e.target.files[0];
    //         var reader = new FileReader();
    //         reader.onload = function (e) {
    //             var img = document.createElement("img");
    //             img.onload = function (event) {
    //                 // Dynamically create a canvas element
    //                 var canvas = document.createElement("canvas");
    //                 // var canvas = document.getElementById("canvas");
    //                 var ctx = canvas.getContext("2d");
    //                 // Actual resizing
    //                 ctx.drawImage(img, 0, 0, 300, 160);
    //                 var dataurl = canvas.toDataURL(imageFile.type);
    //                 document.getElementById("display-image").src = dataurl;
    //             }
    //             img.src = e.target.result;
    //         }
    //         reader.readAsDataURL(imageFile);
    //         if(document.getElementById("no_profile_picture_background")){
    //             document.getElementById("no_profile_picture_background").style.display="none";
    //             document.getElementById("display-image").style.opacity=1;
    //         }
    //     }
    // });

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
    // console.log(varr)
    
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

function charge_categories(){
    // user_like=document.querySelector(`#like-btn-${id_post}`);
    // console.log("esta entrando al charge_categories js")
    fetch(`/categories/`, {
        method: 'POST',
        // data: "stringi",
        // body: JSON.stringify({
            // like_action:"user_like.value"
        // })
    })
    .then(response => response.json())
    .then(result => {
        // console.log(result)
        let categories_list = "";
        let cont_cat = 0
        // console.log(result.categories_array.fields)
        var array = JSON.parse(result.categories_array);
        // var array =Object.values(result.categories_array)
        // console.log("primero");
        // console.log(result.categories_array);
        // console.log("Segundo");
        // console.log(array);

        array.forEach(element => {
            // categories_list += `<li><a href="../category/{{ categories.id }}"> ${element} </a></li>`;
            // console.log("fields field");
            // console.log(element.fields);
            // console.log("fields category name");
            // console.log(element.fields.category_name);
            // console.log("PKk");
            // console.log(element.pk);
            categories_list += `<a href="../category/${element.pk}"><li> ${element.fields.category_name} </li></a>`;
            cont_cat++;
        });
        cont_cat = cont_cat * 2.5;
        // cont_cat = cont_cat + 2.5;
        cont_cat = cont_cat + "rem"
        document.querySelector("#myDropdownCategories > ul").innerHTML = categories_list;
        document.getElementById("myDropdownCategories").style.height = cont_cat;
        // document.querySelector(`#heart-img-${id_post}`).innerHTML
        // setTimeout(function(){ 
        //     document.querySelector(`#heart-img-${id_post}`).innerHTML = '';
        //     if(result.prev_status=="heart_empty"){
        //         document.querySelector(`#heart-img-${id_post}`).innerHTML = '<path d="M33.6751 7.9851C32.7561 7.05963 31.6632 6.32493 30.4593 5.82324C29.2555 5.32155 27.9643 5.06277 26.6601 5.06177C24.1931 5.06217 21.8162 5.98889 20 7.65843C18.1841 5.98861 15.8071 5.06185 13.34 5.06177C12.0343 5.06313 10.7417 5.3227 9.53661 5.82555C8.33155 6.3284 7.23783 7.06459 6.31838 7.99177C2.39672 11.9301 2.39838 18.0901 6.32172 22.0118L20 35.6901L33.6784 22.0118C37.6017 18.0901 37.6034 11.9301 33.6751 7.9851Z" fill="#DA2D57"/>';
        //         document.querySelector(`#like-btn-${id_post}`).value = "heart_full";
        //         document.querySelector(`#like-count-${id_post}`).firstChild.data = result.likers_array.length;
        //     }
        //     else{
        //         document.querySelector(`#heart-img-${id_post}`).innerHTML = '<path d="M20 7.65843C18.1841 5.98861 15.8071 5.06185 13.34 5.06177C12.0343 5.06313 10.7417 5.3227 9.53661 5.82555C8.33155 6.3284 7.23783 7.06459 6.31838 7.99177C2.39672 11.9301 2.39838 18.0901 6.32172 22.0118L18.5417 34.2318C18.825 34.7301 19.3717 35.0518 20 35.0518C20.258 35.0493 20.5119 34.9863 20.7411 34.8679C20.9704 34.7495 21.1686 34.579 21.32 34.3701L33.6784 22.0118C37.6017 18.0884 37.6017 11.9301 33.675 7.9851C32.7561 7.05963 31.6632 6.32493 30.4593 5.82324C29.2555 5.32155 27.9643 5.06277 26.66 5.06177C24.1931 5.06217 21.8162 5.98889 20 7.65843ZM31.3184 10.3418C33.9234 12.9601 33.925 17.0501 31.3217 19.6551L20 30.9768L8.67838 19.6551C6.07505 17.0501 6.07672 12.9601 8.67505 10.3484C9.94172 9.08843 11.5984 8.3951 13.34 8.3951C15.0817 8.3951 16.7317 9.08843 17.9884 10.3451L18.8217 11.1784C18.9764 11.3333 19.16 11.4562 19.3622 11.5401C19.5644 11.6239 19.7812 11.6671 20 11.6671C20.2189 11.6671 20.4357 11.6239 20.6379 11.5401C20.8401 11.4562 21.0237 11.3333 21.1784 11.1784L22.0117 10.3451C24.5317 7.8301 28.8017 7.83677 31.3184 10.3418Z" fill="#3D3D3D"/>';
        //         document.querySelector(`#like-btn-${id_post}`).value = "heart_empty";
        //         document.querySelector(`#like-count-${id_post}`).firstChild.data = result.likers_array.length;
        //     }
        //  }, 200);
    })
    .catch((error) => {
        // alert(error)
        console.log(error)

        // modal_error();
    });
}


function abrir(id) {
    // var file = document.getElementById(id);
    // file.dispatchEvent(new MouseEvent('click', {
    //     view: window,
    //     bubbles: true,
    //     cancelable: true,accept:"image/*"
    // }));

    alert(document.querySelector("#id_create_listing > form > div > input.btn.btn-primary").value)
}
function contar(elem, idGlosa) {
    var glosa = document.getElementById(idGlosa);
    if(elem.files.length == 0) {
        glosa.innerText = "Ningun archivo seleccionado";
    } else {
        glosa.innerText = elem.files.length + "  image selected";
    }
}

function submitButtonClick(event) {
    event.preventDefault();
    //other stuff you want to do instead...

} 