/* #TODO [X] replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: "http://127.0.0.1:5000/api/v1.0", // the running FLASK api server url
  auth0: {
    url: "darthbert-udacity.au.auth0.com", // the auth0 domain prefix
    audience: "Udacity_IAM_API", // the audience set for the auth0 app
    clientId: "YjjkCnzsIK38F1rVy2Gfa6SD90N34iMF", // the client id generated for the auth0 app
    callbackURL: "http://localhost:4200", // the base url of the running ionic application.
  },
};
