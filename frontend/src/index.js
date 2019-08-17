import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { ConnectedRouter } from "connected-react-router";
import store, { history } from "redux/configureStore";
import 'index.css';
import App from 'App';
import "ReactotronConfig";

const rootElement =  document.getElementById('root');


ReactDOM.render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <App />
        </ConnectedRouter>
    </Provider>,
    rootElement
);

