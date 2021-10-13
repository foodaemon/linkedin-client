# Python LinkedIn Client

Python wrapper for the LinkedIn API V2

## Installation

via pip:

```bash
pip install linkedin-client
```

## Usage

```python
from linkedin import linkedin


API_KEY = "YOUR_CLIENT_ID"
API_SECRET = "YOUR_CLIENT_SECRET"
RETURN_URL = "http://localhost:8000"
PERMISSIONS = ["r_basicprofile"]

auth = linkedin.LinkedinOAuth2(API_KEY, API_SECRET, RETURN_URL, PERMISSIONS)
print(auth.authorization_url) # copy this url to your browser
```

When you grant access to the application, you will be redirected to the return url with the following query strings appended to your RETURN_URL:
```http://localhost:8000/?code=YOUR_AUTHORIZATION_CODE```

```python
auth.authorization_code = "YOUR_AUTHORIZATION_CODE"
token = auth.get_access_token()

app = linkedin.LinkedIn(token=token)
print(app.get_profile())
```
