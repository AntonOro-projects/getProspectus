import React, { Component } from "react";
import { connect } from "react-redux";
import { register } from "../actions/root-action";
import { history } from "../helpers/history";

function mapDispatchToProps(dispatch) {
    return {
        register: (url, username, password) => dispatch(register(url, username, password))
    };
}

class ConnectedRegisterPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: ""
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }

    handleChange(event) {
        this.setState({ [event.target.id]: event.target.value });
    }

    handleSubmit(event) {
        event.preventDefault();
        const { username, password } = this.state;
        this.props.register("http://localhost:5000/register", username, password );
        this.setState({ username: "", password: "" } );
    }

    handleClick(event) {
        event.preventDefault();
        history.push("/login");
    }

    render() {
        const { username, password } = this.state;
        return (
            <div>
            <h1>Register here</h1>
            <form onSubmit={this.handleSubmit}>
                <div>
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={this.handleChange}
                    />
                </div>
                <div>
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={this.handleChange}
                    />
                </div>
                <button type="submit">Register</button>
            </form>
                <button type ="button" onClick={this.handleClick}>Go back</button>
            </div>
        );
    }
}

const RegisterPage = connect(null, mapDispatchToProps)(ConnectedRegisterPage);

export default RegisterPage;
