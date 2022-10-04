

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
