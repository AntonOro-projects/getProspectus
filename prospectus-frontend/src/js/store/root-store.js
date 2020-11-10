import { createStore, applyMiddleware, compose } from "redux";
import rootReducer from "../reducers/root-reducer";
import { rootMiddleware } from "../middleware/root-middleware";
import createSagaMiddleware from "redux-saga";
import rootSaga from "../sagas/root-saga";

const initialiseSagaMiddleware = createSagaMiddleware();

const storeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(
  rootReducer,
  storeEnhancers(
    applyMiddleware(rootMiddleware, initialiseSagaMiddleware)
  )
);

initialiseSagaMiddleware.run(rootSaga);

export default store;
