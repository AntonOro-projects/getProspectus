import React, { Component } from "react";
import { connect } from "react-redux";
import {login, thirdPartyLogin} from "../actions/root-action";
import { history } from "../helpers/history";
import { GoogleLogin } from 'react-google-login';
import FacebookLogin from 'react-facebook-login';

function mapDispatchToProps(dispatch) {
    return {
        thirdPartyLogin: (url, token) => dispatch(thirdPartyLogin(url, token)),
        login: (url, username, password) => dispatch(login(url, username, password))
    };
}

class ConnectedLoginPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: ""
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.responseGoogle = this.responseGoogle.bind(this);
        this.responseFacebook = this.responseFacebook.bind(this);
    }

    handleChange(event) {
        this.setState({ [event.target.id]: event.target.value });
    }

    handleSubmit(event) {
        event.preventDefault();
        const { username, password } = this.state;
        this.props.login("http://localhost:5000/login", username, password);
        this.setState({ username: "", password: "" });
    }
    handleClick(event) {
        event.preventDefault();
        history.push("/register");
    }

    responseGoogle(response)  {
        if (!response.error) {
            const token = response.googleId;
            this.props.thirdPartyLogin("http://localhost:5000/thirdpartylogin", token);
        }
    }
    responseFacebook(response) {
        if (response.accessToken) {
            const token = response.accessToken;
            this.props.thirdPartyLogin("http://localhost:5000/thirdpartylogin", token);
        }
    }

    render() {
        const {username, password} = this.state;
        return (
            <div>
                <h1>Login here</h1>
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
                    <button type="submit">Login</button>
                </form>
                <GoogleLogin
                    clientId="270188236823-6fcvb3k624umkr1q8okhr0b3acsmj8n2.apps.googleusercontent.com"
                    buttonText="Login"
                    onSuccess={this.responseGoogle}
                    onFailure={this.responseGoogle}
                    cookiePolicy={'single_host_origin'}

                />
                <FacebookLogin
                    appId="2337685653199134"
                    fields="name,email,picture"
                    callback={this.responseFacebook}
                />
                <button className="float-right" type="button" onClick={this.handleClick}>Go to register page</button>
            </div>
        );
    }
}

const LoginPage = connect(null, mapDispatchToProps)(ConnectedLoginPage);

export default LoginPage;
