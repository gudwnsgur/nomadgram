/* setting, configure my store  */

import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import { connectRouter, routerMiddleware } from 'connected-react-router';
import { createBrowserHistory } from "history";
import { composeWithDevTools } from "redux-devtools-extension";
import users from 'redux/modules/users';



const env = process.env.NODE_ENV;
const history = createBrowserHistory();
const middlewares = [thunk, routerMiddleware(history)];

if (env === "development") {
	const { logger } = require("redux-logger");
	middlewares.push(logger);
}

const reducer = combineReducers({   // combine every reducers
    users,
	router: connectRouter(history)
});


let store;

if (env === "development") {
  store = initialState =>
    createStore(
      reducer, 
      composeWithDevTools(applyMiddleware(...middlewares))
    );
} else {
  store = initialState => createStore(reducer, applyMiddleware(...middlewares));
}

export { history }; // router need history object that I created 

export default store(); // made store with many reducers

// redux middlewares is located in between react application and store
// redux-thunk : let us send actions to our redux sotre when we want 