import { takeEvery, call, put } from "redux-saga/effects";
import {
  API_ERRORED,
  LOGIN_REQUESTED,
  LOGIN_LOADED,
  REGISTER_REQUESTED,
  REGISTER_LOADED, DATA_REQUESTED, DATA_LOADED, THIRD_PARTY_LOGIN_REQUESTED
} from "../constants/action-types";
import { history } from "../helpers/history";

export default function* watcherSaga() {
  yield takeEvery(LOGIN_REQUESTED, loginWorkerSaga);
  yield takeEvery(REGISTER_REQUESTED, registerWorkerSaga);
  yield takeEvery(DATA_REQUESTED, searchWorkerSaga);
  yield takeEvery(THIRD_PARTY_LOGIN_REQUESTED, thirdPartyWorkerSaga);
}

function* loginWorkerSaga(action) {
  try {
    const payload = yield call(getLoginData, action.payload.url, action.payload.username, action.payload.password);
    yield put({ type: LOGIN_LOADED, payload });
  } catch (e) {
    yield put({ type: API_ERRORED, payload: e });
  }
}

function* registerWorkerSaga(action) {
  try {
    const payload = yield call(getRegisterData, action.payload.url, action.payload.username, action.payload.password);
    yield put({ type: REGISTER_LOADED, payload });
  } catch (e) {
    yield put({ type: API_ERRORED, payload: e });
  }
}

function* searchWorkerSaga(action) {
  try {
    const payload = yield call(getSearchData, action.payload.url, action.payload.token, action.payload.search_words, action.payload.exact_match);
    yield put({ type: DATA_LOADED, payload });
  } catch (e) {
    yield put({ type: API_ERRORED, payload: e });
  }
}

function* thirdPartyWorkerSaga(action) {
  try {
    const payload = yield call(thirdPartyLoginFunction, action.payload.url, action.payload.token);
    yield put({ type: LOGIN_LOADED, payload });
  } catch (e) {
    yield put({ type: API_ERRORED, payload: e });
  }
}

function getLoginData(url, username, password) {
  return fetch(url, { dataType: 'json', method: 'GET', headers: {"username": username, "password": password} }).then(response => {
    response.json().then(data =>  {
      if (data.token) {
        localStorage.setItem('user', data.token);
        history.push("/");
      }
    });
  });
}

function getRegisterData(url, username, password) {
  return fetch(url, { dataType: 'json', method: 'GET', headers: {"username": username, "password": String(password)} }).then(response => {
    response.json().then(data =>  {
      console.log(data);
      if (data.success) {
        history.push("/login");
      }
    });
  });
}

function getSearchData(url, token, search_words, exact_match) {
  return fetch(url, { dataType: 'json', method: 'GET', headers: {"token": token, "search_words": search_words, "exact_match": exact_match} }).then(response => response.json())
}

function thirdPartyLoginFunction(url, token) {
  return fetch(url, { dataType: 'json', method: 'POST', headers: {"token": token} }).then(response => {
    response.json().then(data =>  {
      if (data.token) {
        localStorage.setItem('user', data.token);
        history.push("/");
      }
    });
  });
}
