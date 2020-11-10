import { DATA_REQUESTED, LOGIN_REQUESTED, LOGOUT_REQUESTED, REGISTER_REQUESTED, THIRD_PARTY_LOGIN_REQUESTED } from "../constants/action-types";

export function search(url, token, search_words, exact_match) {
  return { type: DATA_REQUESTED, payload: { url, token, search_words, exact_match } };
}

export function login(url, username, password) {
  return { type: LOGIN_REQUESTED, payload: { url, username, password } };
}

export function logout(url, token) {
  return { type: LOGOUT_REQUESTED, payload: { url, token } };
}

export function register(url, username, password) {
  return { type: REGISTER_REQUESTED, payload: { url, username, password } };
}

export function thirdPartyLogin(url, token) {
  console.log(url, token);
  return { type: THIRD_PARTY_LOGIN_REQUESTED, payload: { url, token } };
}