---
page_type: sample
languages:
- python
products:
- azure-active-directory
description: "This sample demonstrates a Python web application calling a Microsoft Graph that is secured using Azure Active Directory."
---
# Integrating Microsoft Identity Platform with a Python web application

1. The python web application uses the Microsoft Authentication Library (MSAL) to obtain a JWT access token from the Microsoft identity platform (formerly Azure AD v2.0):
2. The access token is used as a bearer token to authenticate the user when calling the Microsoft Graph.


### Scenario

This sample shows how to build a Python web app using Flask and MSAL Python,
that signs in a user, and get access to Microsoft Graph.
For more information about how the protocols work in this scenario and other scenarios,
see [Authentication Scenarios for Azure AD](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-authentication-scenarios).

