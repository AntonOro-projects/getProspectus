import React, { Component } from "react";
import { MDBDataTable } from 'mdbreact';
import { connect } from "react-redux";
import { search, logout } from "../actions/root-action";
import { history } from "../helpers/history";

function mapStateToProps(state) {
    return {
        table : state.table
    };
}

function mapDispatchToProps(dispatch) {
    return {
        search: (url, token, search_words, exact_match) => dispatch(search(url, token, search_words, exact_match)),
        logout: (url, token) => dispatch(logout(url, token))
    };
}

class ConnectedSearchPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            search_words: "",
            exact_match: false
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCheckbox = this.handleCheckbox.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }

    handleChange(event) {
        this.setState({ [event.target.id]: event.target.value });
    }

    handleSubmit(event) {
        event.preventDefault();
        const { search_words, exact_match } = this.state;
        const token = localStorage.getItem("user");
        if (search_words) {
            this.props.search("http://localhost:5000/search", token, search_words, exact_match);
            this.setState({search_words: "", exact_match: false});
        }
    }

    handleCheckbox() {
        this.setState({ exact_match: !this.state.exact_match });
    }

    handleClick(event) {
        event.preventDefault();
        const token = localStorage.getItem("user");
        this.props.logout("http://localhost:5000/logout", token);
        history.push("/login");
    }


    render() {
        const { table } = this.props;
        const { search_words, exact_match } = this.state;

        return (
            <div className="container">
                <button type="button" className="btn btn-outline-secondary float-right" onClick={this.handleClick}>Logout
                </button>
                <form className="form-inline mr-auto md-form " onSubmit={this.handleSubmit}>
                    <input
                        className="form-control"
                        aria-label="Search"
                        type="text"
                        placeholder="Search for prospectus"
                        id="search_words"
                        value={search_words}
                        onChange={this.handleChange}
                    />
                    <button className="btn btn-outline-dark" type="submit">Search</button>
                </form>
                <div className="custom-control custom-checkbox">
                    <input
                        type="checkbox"
                        className="custom-control-input"
                        id="exact_match"
                        checked={exact_match}
                        onChange={this.handleCheckbox}
                    />
                    <label
                        className="custom-control-label"
                        data-toggle="tooltip"
                        title="Returns all documents where the search term is matched exactly"
                        htmlFor="exact_match">
                        Exact match
                    </label>
                </div>
                <div id="data">
                    <MDBDataTable
                        striped
                        bordered
                        hover
                        data={table}
                    />
                </div>
            </div>

        );
    }
}

const SearchPage = connect(mapStateToProps, mapDispatchToProps)(ConnectedSearchPage);

export default SearchPage;
