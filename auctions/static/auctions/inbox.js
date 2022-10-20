

document.addEventListener('DOMContentLoaded', function(){

    /* *************** Menu **************** */
    ((d) => {
        const $btnMenu = d.querySelector(".menu-btn"),
          $menu = d.querySelector(".menu");

        $btnMenu.addEventListener("click", (e) => {
            $btnMenu.firstElementChild.classList.toggle("none");
            $btnMenu.lastElementChild.classList.toggle("none");
            $menu.classList.toggle("is-active");
        });

        d.addEventListener("click", (e) => {
            if (!e.target.matches(".menu a")) return false;

            $btnMenu.firstElementChild.classList.remove("none");
            $btnMenu.lastElementChild.classList.add("none");
            $menu.classList.remove("is-active")
        });

    })(document);

    let id_categories = document.getElementById("id_categories");
    if(id_categories)
        charge_categories();

    let inputElement = document.getElementById("input");
    if(inputElement)
        inputElement.addEventListener("change", handleFiles, false);

    function handleFiles() {
        label_button = document.querySelector("#button_image p")
        label_button.classList.add('hide');
        label_button.classList.remove('show');
        let fileList = this.files;
        document.getElementById("image").files = fileList
        document.getElementById("glosaArchivos").innerText = fileList[0].name;
        img = document.getElementById("display-image");
        img.style.display = "block";
        img.src = URL.createObjectURL(fileList[0]);
    }
    
    let new_bid = document.getElementById("new_bid");
    if(new_bid){
        new_bid.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            handleModal()
        }
        });
    }
})

function enable_answer(varr){
    let answer_form = document.getElementById("answer-form-"+varr);
    let add, remove
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
    fetch(`/categories/`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(result => {
        let categories_list = "";
        let cont_cat = 0
        var array = JSON.parse(result.categories_array);

        array.forEach(element => {
            categories_list += `<a href="/category/${element.pk}"><li> ${element.fields.category_name} </li></a>`;
            cont_cat++;
        });
        cont_cat = cont_cat * 2.5;
        cont_cat = cont_cat + "rem"
        document.querySelector("#myDropdownCategories > ul").innerHTML = categories_list;
        document.getElementById("myDropdownCategories").style.height = cont_cat;
    })
    .catch((error) => {
        console.log(error)
    });
}

function contar(elem, idGlosa) {
    var glosa = document.getElementById(idGlosa);
    if(elem.files.length == 0) {
        glosa.innerText = "Ningun archivo seleccionado";
    } else {
        glosa.innerText = elem.files.length + "  image selected";
    }
}

function watch_list_change(id_auction){
    let button_watch_list_change = document.getElementById("in_watchlist")
    if(button_watch_list_change){
        button_watch_list_change.setAttribute('id', 'out_watchlist');
    }else{
        button_watch_list_change = document.getElementById("out_watchlist");
        button_watch_list_change.setAttribute('id', 'in_watchlist');
    }
    fetch(`/add_in_watch_list/${id_auction}/`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.change_response)
    })
    .catch((error) => {
        console.log(error)
    });
}

function magnify(imgID, zoom) {
    var img, glass, w, h, bw;
    img = document.getElementById(imgID);
    /*create magnifier glass:*/
    glass = document.getElementById("id_glass");
    glass.classList.add('show');
    glass.classList.remove('hide');

    /*insert magnifier glass:*/
    img.parentElement.insertBefore(glass, img);
    /*set background properties for the magnifier glass:*/
    glass.style.backgroundImage = "url('" + img.src + "')";
    glass.style.backgroundRepeat = "no-repeat";
    glass.style.backgroundSize = (img.width * zoom) + "px " + (img.height * zoom) + "px";
    bw = 3;
    w = glass.offsetWidth / 2;
    h = glass.offsetHeight / 2;
    /*execute a function when someone moves the magnifier glass over the image:*/
    glass.addEventListener("mousemove", moveMagnifier);
    img.addEventListener("mousemove", moveMagnifier);
    /*and also for touch screens:*/
    glass.addEventListener("touchmove", moveMagnifier);
    img.addEventListener("touchmove", moveMagnifier);
    function moveMagnifier(e) {
      var pos, x, y;
      /*prevent any other actions that may occur when moving over the image*/
      e.preventDefault();
      /*get the cursor's x and y positions:*/
      pos = getCursorPos(e);
      x = pos.x;
      y = pos.y;
      /*prevent the magnifier glass from being positioned outside the image:*/
      if (x > img.width - (w / zoom)) {x = img.width - (w / zoom);}
      if (x < w / zoom) {x = w / zoom;}
      if (y > img.height - (h / zoom)) {y = img.height - (h / zoom);}
      if (y < h / zoom) {y = h / zoom;}
      /*set the position of the magnifier glass:*/
      glass.style.left = (x - w) + "px";
      glass.style.top = (y - h) + "px";
      /*display what the magnifier glass "sees":*/
      glass.style.backgroundPosition = "-" + ((x * zoom) - w + bw) + "px -" + ((y * zoom) - h + bw) + "px";
    }
    function getCursorPos(e) {
      var a, x = 0, y = 0;
      e = e || window.event;
      /*get the x and y positions of the image:*/
      a = img.getBoundingClientRect();
      /*calculate the cursor's x and y coordinates, relative to the image:*/
      x = e.pageX - a.left;
      y = e.pageY - a.top;
      /*consider any page scrolling:*/
      x = x - window.pageXOffset;
      y = y - window.pageYOffset;
      return {x : x, y : y};
    }
}

function close_magnify(){
    let glass = document.getElementById("id_glass");
    if(glass){
        glass.classList.add('hide');
        glass.classList.remove('show');
    }
}