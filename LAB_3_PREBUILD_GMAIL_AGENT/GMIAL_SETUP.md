### 3.1 Gmail — Google OAuth2 Credentials

You need a **Google Cloud Project** with the Gmail API enabled, plus an OAuth2 Client ID and Secret.

#### Step 1 — Create a Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click the project dropdown (top left) → **New Project**
3. Enter a name (e.g., `watsonx-orchestrate-gmail`) → click **Create**
4. Make sure the new project is selected in the dropdown

#### Step 2 — Enable the Gmail API

1. In the left menu go to **APIs & Services → Library**
2. Search for `Gmail API`
3. Click **Gmail API** → click **Enable**


#### Step 3 — Configure the OAuth Consent Screen

1. Go to **APIs & Services → OAuth consent screen**
2. Select **External** → click **Create**
3. Fill in:
   - App name: `watsonx Orchestrate`
   - User support email: your Gmail address
   - Developer contact email: your Gmail address
4. Click **Save and Continue** through the remaining screens (Scopes and Test users can be left default for now)
5. Click **Back to Dashboard**
6. Go to **Audience** → **Test users**
7. Add your Gmail address  → Save

#### Step 4 — Create OAuth2 Credentials

1. Go to **APIs & Services → Credentials**
2. Click **+ Create Credentials → OAuth client ID**
3. Application type: **Web application**
4. Name: `watsonx-orchestrate-client`
5. Under **Authorized redirect URIs**, click **+ Add URI** and enter:
   ```
   https://iam.cloud.ibm.com/identity/oauth/callback
   https://us-south.watson-orchestrate.cloud.ibm.com/mfe_connectors/api/v1/agentic/oauth/_callback
   ```
   > This is the IBM Cloud OAuth callback URL that Orchestrate uses to complete the OAuth flow.
6. Click **Create**
7. A dialog will show your credentials — **copy and save both values immediately:**

```
Client ID:      xxxxxxxxxxxxxxxx.apps.googleusercontent.com
Client Secret:  GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxx
```

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
