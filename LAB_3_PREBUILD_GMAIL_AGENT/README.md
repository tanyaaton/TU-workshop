1. do to `Discovery` page, search for google pre-built agent
2. choose "Email manager"
3. click in tools > connection
4. configure connection as follow:


#### Credentials Summary (Gmail)

```
Authentication type:   OAuth2 Authorization Code
Server URL:            https://gmail.googleapis.com/
Token URL:             https://oauth2.googleapis.com/token
Authorization URL:     https://accounts.google.com/o/oauth2/v2/auth
Client ID:             (from Step 4 above)
Client Secret:         (from Step 4 above)
Scope:                 https://mail.google.com/
Token request field:   prompt = consent
Auth request fields:   base_url = https://gmail.googleapis.com/
                       access_type = offline
```


try the following prompt:

```
send email to <your email> with 
topic: Your dental appointment
content: we have already scheduled your appointment
```

