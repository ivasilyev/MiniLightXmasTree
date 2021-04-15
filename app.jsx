class App extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
          animation: "",
          colors: [],
          pause: 0
      };
      this.render_form = this.render_form.bind(this);
    }

        setState(state) {
        if (Object.keys(state).length > 0) {
            this.state = state;
            this.render();
        }
    }

    send_get_query(json) {
        let xhr = new XMLHttpRequest();
        let url = `url?data=${encodeURIComponent(JSON.stringify(json))}`;
        xhr.open("GET", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                let state = JSON.parse(xhr.responseText);
                console.log('send_get_query', state);
            }
        };
        xhr.send();
    }


    render_form() {
        return (
            <div className="container" role="main">
                <div className="py-5 text-center">
                    <h2>Mini Light Christmas Tree</h2>
                    <h4>Control panel</h4>
                </div>

                <form className="form-signin needs-validation" noValidate="" id="" name="">
                    <fieldset>
                        <div className="form-label-group">
                            <label htmlFor="animation_dropdown">Select an animation:</label>
                            <select className="custom-select d-block w-100"
                                    id="label__animation_dropdown" required>
                                <option selected disabled value="">Select...</option>
                                <option value="random_blink">random_blink</option>
                                <option value="bounce2">bounce2</option>
                                <option value="cycle2">cycle2</option>
                            </select>
                        </div>

                        <div className="form-label-group">
                            <label htmlFor="label__range_delay">Select switching delay:</label>
                            <input type="range" min="1" max="1000" value="10" step="1" id="label__range_delay" />
                            <input type="text" id="input__delay" />
                        </div>
                        <div className="form-label-group">
                        </div>

                        <div className="checkbox mb-3">
                            <label htmlFor="always_lit__checkbox">Keep pixels on?</label>
                            <input type="checkbox" id="always_lit__checkbox" />
                        </div>


                        <div className="order-md-1">
                            <div className="row">
                            </div>
                        </div>
                    </fieldset>

                    <button className="btn btn-lg btn-primary btn-block" type="submit">Set</button>
                    <button className="btn btn-lg btn-primary btn-block" id="button__revert">Reset</button>
                </form>

                <p className="mt-5 mb-3 text-muted text-center">© 2021</p>
            </div>
        );
    }


    render() {
        return this.render_form();
    }
}

ReactDOM.render(<App />, document.getElementById('root'));
