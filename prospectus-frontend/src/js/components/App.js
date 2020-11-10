import React from "react";
import SearchPage from "./SearchPage";
import LoginPage from "./LoginPage";
import RegisterPage from "./RegisterPage";
import PrivateRoute from "./PrivateRoute";
import { history } from "../helpers/history"
import 'bootstrap/dist/css/bootstrap.min.css';

import { Router, Route, Switch, Redirect } from "react-router-dom";

const App = () => (
    <div className="jumbotron">
        <div className="container">
            <Router history={history}>
                <Switch>
                    <PrivateRoute exact path="/" component={SearchPage}/>
                    <Route path="/login" component={LoginPage}/>
                    <Route path="/register" component={RegisterPage}/>
                    <Redirect from="*" to="/"/>
                </Switch>
            </Router>
        </div>
    </div>
);

export default App;
