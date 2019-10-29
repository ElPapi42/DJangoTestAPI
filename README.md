# DJangoTestAPI
Student project, sharpen my skills on django framework for back-end development

## Usage

##### rest_api/register
register a new user to the db

Method: POST

Args: str:username, str:email, str:password

##### rest_api/login
login user, if registered on the db

Method: POST

Args: str:username, str:password

##### rest_api/logout
logout an user, if has active sessions

Method: POST

Args: --

##### rest_api/user/<str:username>
return the data associated with the argument name

Method: GET

Args: str:username
