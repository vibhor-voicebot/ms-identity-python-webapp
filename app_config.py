import os

CLIENT_ID = "991ad49c-e439-43bc-b975-2224fb8cf899" # Application (client) ID of app registration
TENANT_ID = "02f3ad0f-cc97-4a02-b9d8-75e8ddfbea03"
CLIENT_SECRET = "E8Un0k2DJ1Bv_hELC.zKY7_Fjww4TgUi-L" # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

##########commenting 1st and uncommenting 2nd for testing 
#AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
AUTHORITY = "https://login.microsoftonline.com/02f3ad0f-cc97-4a02-b9d8-75e8ddfbea03"

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

##########adding for testing 
GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0/me'

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All"]

##########adding for testing 
DELEGATED_PERMISSONS = ["User.Read"]
AAD_ROLE_CHECK = False


SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session
