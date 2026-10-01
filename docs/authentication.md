# Authentication

Yaptide platform can authenticate users using two methods:

  * using own database of users. In that case submission of simulation is limited only to a local pool of workers.
  * using Keycloak server. Such server is provided for example in PLGrid infrastructure. This solution offers a possibility to submit simulations to an HPC cluster.


Configuration of keycloak is based on following environmental variables, for backend:

  * `KEYCLOAK_BASE_URL` - URL of the keycloak server, for example `'https://sso.pre.plgrid.pl'`
  * `KEYCLOAK_REALM` - name of the realm, for example `PLGrid`
  * `KEYCLOAK_CLIENT_ID` - name of the client, for example `yaptide`

The frontend uses following names:

  * `REACT_APP_KEYCLOAK_BASE_URL` - URL of the keycloak server, for example `'https://sso.pre.plgrid.pl'`
  * `REACT_APP_KEYCLOAK_REALM` - name of the realm, for example `PLGrid`
  * `REACT_APP_KEYCLOAK_CLIENT_ID` - name of the client, for example `yaptide`

The `REACT_APP_` prefix is required by the create-react-app tool, see https://create-react-app.dev/docs/adding-custom-environment-variables

These variables needs to be provided to the docker compose files via the `.env` file, both for backend and the frontend parts.
The backend propagates this variable to the `yaptide_flask` container, to be able to verify keycloak tokens.
The frontend needs to know the URL of the keycloak server, so it can redirect the user to the login page.
To properly setup these variables in case of ansible deployment, please use `yap_dev_vars.yml` as an example.

## Keycloak-only instances

Local users (the first method) can be switched off on the backend with these variables in the backend `.env` file:

  * `ENABLE_USER_REGISTRATION` - set to `false` to block self-registration of local users; existing local users can still log in. The docker compose file defaults it to `false`.
  * `ENABLE_LOCAL_USERS` - set to `false` to allow only Keycloak users: local users can neither register nor log in, and their existing sessions are rejected. Defaults to `true`.

The frontend needs no extra setting: it asks the backend whether local users are enabled and hides the "use password login" option when they are not.
