import { DATA_PROCESSED, DATA_LOADED, LOGOUT_REQUESTED} from "../constants/action-types";
import React from "react";

export function rootMiddleware({ dispatch }) {
  return function(next) {
    return function(action) {
      if (action.type === LOGOUT_REQUESTED) {
        fetch(action.payload.url, {
          dataType: 'json',
          method: 'POST',
          headers: {"token": action.payload.token}
        }).then(r =>r.json());
        localStorage.removeItem('user')
        return dispatch({ type: "LOGGED_OUT_USER"});
      }

      if (action.type === DATA_LOADED) {
        action.payload.forEach(element => {
          const download_pdf = "http://localhost:5000/download/" + element.download_link;
          const open_pdf = "http://localhost:5000/pdf/" + element.download_link;
          element.download_link = <a href={download_pdf} target='_blank' rel="noopener noreferrer">Do it!</a>;
          element.open_in_browser = <a href={open_pdf} target='_blank' rel="noopener noreferrer">Do it!</a>;
        })
        return dispatch({ type: DATA_PROCESSED, payload: action.payload});
      }

      return next(action);
    };
  };
}
