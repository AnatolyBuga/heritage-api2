import React from "react";
import ReactDOM from "react-dom";
import { Route, Switch } from "react-router-dom";
import { store, persistor, history } from 'redux/store';
import { Provider } from "react-redux";
import { ConnectedRouter  } from "connected-react-router";
import { PersistGate } from "redux-persist/integration/react";

import "assets/scss/material-dashboard-pro-react.scss?v=1.9.0";
import PrivateRoute from "components/PrivateRoute";
import Layout from "containers/Layout";
import Login from "containers/Auth/LoginPage";
import Register from "containers/Auth/RegisterPage";

ReactDOM.render(
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <ConnectedRouter  history={history}>
        <React.Fragment>
          <Switch>
            <Route exact path="/login" component={Login}/>
            {/*<Route exact path="/login/email_verification" component={EmailVerification}/>*/}
            <Route exact path="/register" component={Register}/>
            {/*<Route exact path="/reset_password" component={ResetPasswordEmail}/>*/}
            {/*<Route exact path="/auth/reset_password" component={ResetPassword}/>*/}
            <PrivateRoute path="/" component={Layout}/>
          </Switch>
          {/*<ReduxToastr timeOut={3000} transitionIn="fadeIn" transitionOut="fadeOut"/>*/}
        </React.Fragment>
      </ConnectedRouter>
    </PersistGate>
  </Provider>,
  document.getElementById("root")
);