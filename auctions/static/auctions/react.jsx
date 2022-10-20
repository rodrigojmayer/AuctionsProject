let modal = document.getElementById("modal")
if(modal)
    ReactDOM.render(<Modal />, modal);

function Modal(){
    return(
        <div id="id_modal" class="modal-alert hide" >
            <div id="id_modal_body" class="modal-body ">
                <div id="id_close_button">
                    <svg name="close" width="16" height="16" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path name="close" d="M21.1987 8L15.5413 13.656L9.88533 8L8 9.88533L13.656 15.5413L8 21.1973L9.88533 23.0827L15.5413 17.4267L21.1987 23.0827L23.084 21.1973L17.428 15.5413L23.084 9.88533L21.1987 8Z" fill="#D90062"/>
                    </svg>
                </div>
                <h5 id="modal_subtitle"></h5>
                <p id="modal_text"></p>
                <div class="flex-horizontal">
                    <button id="modal_back"  class="btn btn-primary" type="button" value="Back" >Back</button>
                    <button id="modal_save" class="btn btn-primary" value="Save" name="_save" >Save</button>
                </div>
                <div id="modal_image"></div>
            </div>
        </div>
    ) 
}

// -------JS SCRIPT-------- //

let modal_alert = document.querySelector(".modal-alert");
let accept = document.getElementById("accept");
if(accept){
    accept.addEventListener("click", (e)=>{       
        let ew = false
        handleModal(ew)
    }, false)
}

let article_image = document.getElementById("article_image")
if(article_image){
    article_image.addEventListener("click", (e)=>{
        let ew = true
        handleModal(ew)
    }, false)
};
 
function handleModal(evt) {
    modal_alert.classList.add('show');
    modal_alert.classList.remove('hide');
    lockScroll()
    let id_modal = document.getElementById("id_modal");
    let id_modal_body = document.getElementById("id_modal_body");
    let modal_subtitle = document.getElementById("modal_subtitle");
    let modal_text = document.getElementById("modal_text");
    let modal_back = document.getElementById("modal_back");
    let modal_save = document.getElementById("modal_save");
    let modal_image = document.getElementById("modal_image");
    let id_close_button = document.getElementById("id_close_button");
    let value

    if(evt)   // for the img modal
        value = "modal_image"
    else
        value = modal.getAttribute('value')

    if(modal_save){
        modal_save.addEventListener("click", submitButtonClick)
    }

    if(value == "create_listing"){
        let data_article = document.getElementById("data_article");
        let data_description = document.getElementById("data_description");
        let data_initial_price = document.getElementById("data_initial_price");
        let data_auction_category = document.getElementById("data_auction_category");
        let data_image = document.getElementById("image");
        let modal_answer_text = ""

        if(!data_article.value){
            modal_answer_text += "- Name</br>"
        }
        if(!data_description.value){
            modal_answer_text += " - Description</br>"
        }
        if(!data_initial_price.value){
            modal_answer_text += " - Price</br>"
        }
        if(!data_auction_category.value){
            modal_answer_text += " - Category</br>"
        }
        if(!data_image.value){
            modal_answer_text += " - Image</br>"
        }
        if(modal_answer_text){
            modal_subtitle.innerHTML = "Missing data"
            modal_text.innerHTML = `You need to enter: </br> ${modal_answer_text}`
            rejected_modal()
        }
        else{
            const formData = new FormData();
            if(data_article)
                formData.append('name', data_article.value);
            formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
            fetch(`/check_auction/`, {
                method: 'POST',
                body:formData,
            })
            .then(response => response.json())
            .then(result => {
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
                }
            })
            .catch((error) => {
                console.log(error)
            });
        }
    }
    else if( value == "listing_page"){
        let bid_price = parseInt(document.getElementById("bid_price").getAttribute('value'))
        if(!bid_price)
            bid_price = parseInt(document.getElementById("auction_price").getAttribute('value'))
        const new_bid = parseInt(document.getElementById("new_bid").value)
        if(bid_price < new_bid){
            modal_subtitle.innerHTML = "New bid"
            modal_text.innerHTML = "You are offering $" + new_bid
            modal_subtitle.classList.add('show');
            modal_subtitle.classList.remove('hide');
            modal_text.classList.add('show');
            modal_text.classList.remove('hide');
            modal_back.classList.add('show');
            modal_back.classList.remove('hide');
            modal_save.classList.add('show');
            modal_save.classList.remove('hide');
            modal_image.classList.add("hide");
            modal_image.classList.remove("show");
            id_modal_body.classList.remove("modal-body-bigger")
        }
        else{
            modal_subtitle.innerHTML = "Not enough"
            modal_text.innerHTML = "Your offer must be higher than $" + bid_price
            modal_subtitle.classList.add('show');
            modal_subtitle.classList.remove('hide');
            modal_text.classList.add('show');
            modal_text.classList.remove('hide');
            modal_back.classList.remove('hide');
            modal_back.classList.add('show');
            modal_image.classList.add("hide");
            modal_image.classList.remove("show");
            id_modal_body.classList.remove("modal-body-bigger")
            rejected_modal()
        }
    }
    else if( value == "modal_image"){
        modal_image.innerHTML = `<img src=${modal.getAttribute('src')}  height="200px" />`
        modal_subtitle.classList.add('hide');
        modal_subtitle.classList.remove('show');
        modal_text.classList.add('hide');
        modal_text.classList.remove('show');
        modal_back.classList.add('hide');
        modal_back.classList.remove('show');
        modal_save.classList.add('hide');
        modal_save.classList.remove('show');
        modal_image.classList.add("show");
        modal_image.classList.remove("hide");
        id_modal_body.classList.add("modal-body-bigger")
    }
    id_modal.addEventListener("click", (e)=>{
        if (e.target.matches("#id_modal") || e.target.getAttribute('name') == 'close'){
            closeModal()
        }
    })
    id_close_button.addEventListener("click", closeModal)
    modal_back.addEventListener("click", closeModal)
    function closeModal(){
        modal_alert.classList.add('hide');
        modal_alert.classList.remove('show');
        unLockScroll()
    }
    function rejected_modal(){
        modal_save.classList.remove('show');
        modal_save.classList.add('hide');
    }
};
function lockScroll(){
    document.body.classList.add("lock-scroll");
    document.body.classList.remove("un-lock-scroll");
}
function unLockScroll(){
    document.body.classList.remove("lock-scroll")
    document.body.classList.add("un-lock-scroll")
}
function submitButtonClick() {
    document.getElementById("myForm").submit();
}