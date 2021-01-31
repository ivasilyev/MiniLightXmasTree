class App extends React.Component {
    constructor(props) {
      super(props);
      this.state = {};
      this.render_form = this.render_form.bind(this);
    }

    render_form() {
        return (
            <div class="container">
                <div class="py-5 text-center">
                    <h2>Mini Light Christmas Tree</h2>
                    <h4>Control panel</h4>
                    <p class="lead"></p>
                </div>
                <form class="needs-validation" novalidate="" id="" name="">
                    <fieldset>
                        <div class="order-md-1">
                            <div class="row">
                                <label for="animation_dropdown">Select an animation:</label>
                                <select class="custom-select d-block w-100" id="animation_dropdown" required>
                                    <option selected disabled value="">Select...</option>
                                    <option value="random_blink">random_blink</option>
                                    <option value="bounce2">bounce2</option>
                                    <option value="cycle2">cycle2</option>
                                </select>
                            </div>
                        </div>
                    </fieldset>
                </form>
            </div>
        );
    }


    render() {
        return this.render_form();
    }
}

ReactDOM.render(<App />, document.getElementById('root'));
