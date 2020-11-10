import { DATA_PROCESSED, API_ERRORED, LOGIN_LOADED, REGISTER_LOADED } from "../constants/action-types";

const initialState = {
  users: [],
  registered: [],
  table : {
    columns: [
      {
        label: 'Date',
        field: 'date',
        sort: 'asc',
        width: 150
      },
      {
        label: 'Company name',
        field: 'company_name',
        sort: 'asc',
        width: 270
      },
      {
        label: 'Type',
        field: 'type',
        sort: 'asc',
        width: 200
      },
      {
        label: 'Download link',
        field: 'download_link',
        sort: 'asc',
        width: 100
      },
      {
        label: 'Open in browser',
        field: 'open_in_browser',
        sort: 'asc',
        width: 150
      }
    ],
    rows: []
  }
};

function rootReducer(state = initialState, action) {

  if (action.type === DATA_PROCESSED) {
    return Object.assign({}, state, {
      table: Object.assign({}, state.table, {
        rows : action.payload
      })
    });
  }

  if (action.type === API_ERRORED) {
    return Object.assign({}, state, {
      remoteArticles: state.remoteArticles.concat(action.payload)
    });
  }

  if (action.type === LOGIN_LOADED) {
    return Object.assign({}, state, {
      users: state.users.concat(action.payload)
    });
  }

  if (action.type === REGISTER_LOADED) {
    return Object.assign({}, state, {
      registered: state.registered.concat(action.payload)
    });
  }
  return state;
}

export default rootReducer;
