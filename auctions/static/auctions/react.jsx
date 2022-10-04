    function App(){
        const [state, setState] = React.useState({
            num1: Math.ceil(Math.random() * 10),
            num2: Math.ceil(Math.random() * 10),
            response: "",
            score: 0,
            incorrect: false,
        })
        function updateResponse(event){
            setState({
                ...state,
                response: event.target.value,
            })
        }
        function inputKeyPress(event){
            // console.log(event.key)
            if(event.key == "Enter"){
                let answer = parseInt(state.response)
                if(state.num1 + state.num2 === answer){
                    setState({
                        ...state,
                        score: state.score+1,
                        response: "",
                        num1: Math.ceil(Math.random() * 10),
                        num2: Math.ceil(Math.random() * 10),
                        incorrect: false,
                    })
                }
                else{
                    setState({
                        ...state,
                        score: state.score-1,
                        response: "",
                        incorrect: true,
                    })
                } 
            }
        }
        if(state.score === 10 ){
            return(
                <div id="winner">
                    You won!!!
                </div>
            )
        }
        return(
            <div>
                <div id="problem" class={state.incorrect ? "incorrect" : ""} > {state.num1} + {state.num2}</div>
                <input  onKeyPress={inputKeyPress} onChange={updateResponse} value={state.response}/>
                <div>Score: {state.score} </div>
            </div>
        );
    }

    // let app = document.querySelector("#app")
    // if(app)
        // ReactDOM.render(<App />, document.querySelector("#app"));





// var modal = document.querySelector("#modal")
var modal = document.getElementById("modal")
if(modal)
    ReactDOM.render(<Modal />, modal);
        
        

function Modal(){

    // console.log(modal.getAttribute('value'))
    
    return(
        <div class="modal-alert hide" >
            <div class="modal-body ">
                <h5 id="modal_subtitle"></h5>
                <p id="modal_text"></p>
                <div class="flex-horizontal">
                    <button id="modal_back"  class="btn btn-primary" type="button" value="Back" >Back</button>
                    <input id="modal_save" onclick="submitButtonClick(event)" class="btn btn-primary" type="submit" value="Save" name="_save" />
                </div>
            </div>
        </div>
    )

    // else if(modal.getAttribute('value') == "listing_page"){

        // return()
    // }
    // if(modal.getAttribute('value') == "listing_page"){
    // }


}



    

// -------JS SCRIPT-------- //

let modal_alert = document.querySelector(".modal-alert");
console.log(modal_alert)
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
    
    console.log("modal value")
    console.log(modal.getAttribute('value'))
    if(modal.getAttribute('value') == "create_listing"){
        let data_article = document.getElementById("data_article");
        let data_description = document.getElementById("data_description");
        let data_initial_price = document.getElementById("data_initial_price");
        let data_auction_category = document.getElementById("data_auction_category");
        let data_image = document.getElementById("image");
        let modal_answer_text = ""
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
            if(data_article)
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
    }

    else if( modal.getAttribute('value') == "listing_page"){

        // new_bid
        const bid_price = document.getElementById("bid_price")
        // console.log("inicial price: " + bid_price.getAttribute('value'))
        const new_bid = document.getElementById("new_bid")
        // console.log("new bid: " + new_bid.value)
        if(bid_price.getAttribute('value') < new_bid.value){
            modal_subtitle.innerHTML = "Duplicate data"
            modal_text.innerHTML = "There is already an active article with that name."
            rejected_modal()

        }
            
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