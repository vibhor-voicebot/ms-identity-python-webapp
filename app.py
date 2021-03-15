import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config



from flask import Flask, render_template, request
from flask import Flask, jsonify, request, render_template
import socket, os, json, sys
import requests
import random, os
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
import subprocess
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql
import mysql.connector
import sys, getopt
import pymysql
import subprocess
from subprocess import PIPE, run
import sys,os
from azure.cli.core import get_default_cli
from flask import Flask, jsonify, request, render_template
import socket, os, json, sys
import requests
import random, os
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
import subprocess

#Use the get_client_from_auth_file method to create the client object:
from azure.common.client_factory import get_client_from_auth_file
from azure.mgmt.resource import SubscriptionClient
import sys, yaml
from flask import send_file, send_from_directory, safe_join, abort, Response


######## New libs added
import pyodbc
import struct
import adal
from msrestazure.azure_active_directory import AADTokenCredentials


app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    print ("Printing the User details from Session ++++++++++++++++++")
    user=session["user"]
    organization = ""
    organization = str(str(str(user.get('preferred_username')).split("@")[1]).split(".com")[0])
    print (user)

    return render_template('index.html', user=session["user"], organization=organization, ansibleOutput="", version=msal.__version__)

#@app.route("/login")
#def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
#    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
#    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)


@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())

    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = _build_auth_url(scopes=app_config.DELEGATED_PERMISSONS, state=session["state"])
    return render_template("login.html", auth_url=auth_url, version=msal.__version__)


#@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
#def authorized():
#    try:
#        cache = _load_cache()
#        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
#            session.get("flow", {}), request.args)
#        if "error" in result:
#            return render_template("auth_error.html", result=result)
#        session["user"] = result.get("id_token_claims") 
#        print ("Printing complete result object here +++++++++++++++++")
#        print (result)
#        _save_cache(cache)
#    except ValueError:   
#        pass  # Simply ignore them
#    return redirect(url_for("index"))



@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("index"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=app_config.DELEGATED_PERMISSONS,  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("authorized", _external=True))
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

#@app.route("/graphcall")
#def graphcall():
#    token = _get_token_from_cache(app_config.SCOPE)
#    if not token:
#        return redirect(url_for("login"))
#    graph_data = requests.get(  # Use token to call downstream service
#        app_config.ENDPOINT,
#        headers={'Authorization': 'Bearer ' + token['access_token']},
#        ).json()
#    return render_template('display.html', result=graph_data)


@app.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(app_config.DELEGATED_PERMISSONS)
    if not token:
        return redirect(url_for("login"))

    graph_data = requests.get(  # Use token to call downstream service
        app_config.GRAPH_ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)


@app.route('/startup', methods =['GET', 'POST'])
def startup():
    dataout = dict()
    msg = ""
    ansibleOutput = ""
    if request.method == 'POST' and 'ProjectName' in request.form and 'Organization' in request.form:
      try:
        orgName = request.form['Organization'] or ""
        projName = request.form['ProjectName'] or ""
        username = request.form['User'] or ""
        DevOpsPipelineActions = ""
        hiddenValue = request.form['hidden'] or ""
        PipelineName = request.form['PipelineName'] or ""
        ProjectStack = ""
        Repository = ""
        if "createpipeline" in hiddenValue :
            ProjectStack = str(request.form['ProjectStack']).lower() or ""
            Repository = request.form['Repository'] or ""
        servicePrincipalName = "GenpactForOUs-WmPrivateCloud-SP"
        clientID = "12345678-1111-2222-3333-1234567890ab"
        clientSecret = "abcdef00-4444-5555-6666-1234567890ab"
        tenantID = "00112233-7777-8888-9999-aabbccddeeff"
        objectID = "aa11bb33-cc77-dd88-ee99-0918273645aa"
        resourceGroupName = "rg-WMPrivateCloud"
        devopsOrgName = "GenpactForOUs"
        devopsProject = projName
        pat = "s47aonaphsftczamwp4gilgcfwts73diilsvvrcaknmhkhrtqzwa"
        msg = orgName+' | '+projName
        hiddenValue = request.form['hidden'] or ""


        NewDecription = ""
        NewBranch = "master"
        NewPipelineName = ""

        if "createpipeline" in hiddenValue.lower() :
            DevOpsPipelineActions = "createpipeline"
        if "runpipeline" in hiddenValue.lower() :
            DevOpsPipelineActions = "runpipeline"
        if "updatepipeline" in hiddenValue.lower() :
            DevOpsPipelineActions = "updatepipeline"
            NewDecription1 = request.form.get('NewDecription')
            if (NewDecription1) :
                NewDecription = request.form['NewDecription']
            NewBranch1 = request.form.get('NewBranch')
            if (NewBranch1) : 
                NewBranch = request.form['NewBranch']
            NewPipelineName1 = request.form.get('NewPipelineName')
            if (NewPipelineName1) :
                NewPipelineName = request.form['NewPipelineName']
        if "deletepipeline" in hiddenValue.lower() :
            DevOpsPipelineActions = "deletepipeline"
        #conn = pymysql.connect(user='myadmin@ansibledemoserver', password='Feb@2021', host='ansibledemoserver.mysql.database.azure.com', database='defaultdb', ssl= {'ssl': {'ca': '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'}})
        #Creating a cursor object using the cursor() method
        #cursor = conn.cursor()
        #cursor.execute('SELECT * FROM ClientsMappingVault WHERE orgName = {} AND projectName = {}').format(orgName, projName)
        print ("Checking for Service principals mapping in Azure MySQL table")
        #print ('SELECT * FROM ClientsMappingVault WHERE orgName = {} AND projectName = {}')).format(orgName, projName)
        print ('SELECT * FROM ClientsMappingVault WHERE orgName ='+orgName+' AND projectName ='+projName)
        #result = cursor.fetchone()
        #if result:
            #servicePrincipalName = result['servicePrincipalName']
            #clientID = result['clientID']
            #clientSecret = result['clientSecret']
            #tenantID = result['tenantID']
            #objectID = result['objectID']
            #resourceGroupName = result['resourceGroupName']
            #devopsOrgName = result['devopsOrgName'] #this will be same as OrgName for now and will be saved in DB when admin user submits the onboarding operation + he has to additonally create devops org on dev.azure.com UI and generate PAT token which will make ajax call from onboarding webpage (psot submitting mapping details in DB) to save PAT against the row(s) with matching OrgName
            #devopsProject = result['devopsProject'] # this will saved with same value as what ProjectName is saved when admin saves the details in DB along with Org & DevOps OrgName
            #pat = result['PAT']

        # Calling Ansible Playbook here that will login as ServicePrincipal credentials, then based on DevOps action type run the az create/update/run pipeline workflows
        cmd = "ansible-playbook ./ansible_automation/azure_linux_playbook.yml -vv --extra-vars=\"orgName={orgName} projName={projName} username={username} DevOpsPipelineActions={DevOpsPipelineActions} PipelineName={PipelineName} ProjectStack={ProjectStack} Repository={Repository} servicePrincipalName={servicePrincipalName} clientID={clientID} clientSecret={clientSecret} tenantID={tenantID} objectID={objectID} resourceGroupName={resourceGroupName} devopsOrgName={devopsOrgName} devopsProject={devopsProject} pat={pat} NewDecription={NewDecription} NewBranch={NewBranch} NewPipelineName={NewPipelineName}\"".format(orgName=orgName,projName=projName,username=username,DevOpsPipelineActions=DevOpsPipelineActions,PipelineName=PipelineName,ProjectStack=ProjectStack,Repository=Repository,servicePrincipalName=servicePrincipalName,clientID=clientID,clientSecret=clientSecret,tenantID=tenantID,objectID=objectID,resourceGroupName=resourceGroupName, devopsOrgName=devopsOrgName, devopsProject=devopsProject, pat=pat,NewDecription=NewDecription,NewBranch=NewBranch,NewPipelineName=NewPipelineName)
        print (cmd)
        ansibleOut = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        ansibleOutput = ansibleOut.stdout.read()
        print (ansibleOutput)


 
###########################################################################################################
        if "createpipeline" in DevOpsPipelineActions :
            if "failed=0" in str(ansibleOutput) and "unreachable=0" in str(ansibleOutput) :
                msg = "Devops Pipeline -"+PipelineName+" is created for project -"+devopsProject
            else :
                msg = "Failed to create Devops Pipeline -"+PipelineName+" for project -"+devopsProject+" check console logs for debugging"
            dataout["msg"] = msg
            dataout["ansibleOutput"] = str(ansibleOutput)


        ansibleOutput = str(ansibleOutput).replace('"', '')
        ansibleOutput = str(ansibleOutput).replace("'", '')
        ansibleOutput = str(ansibleOutput).replace("}", '')
        ansibleOutput = str(ansibleOutput).replace("{", '')
        ansibleOutput = str(ansibleOutput).replace("=>", '')
        ansibleOutput = str(ansibleOutput).replace("*", '')
        ansibleOutput = str(ansibleOutput).replace("[", '')
        ansibleOutput = str(ansibleOutput).replace("]", '')
        ansibleOutput = str(ansibleOutput).replace(",", '')
        #ansibleOutput = str(ansibleOutput).replace("#", '')
        ansibleOutput = str(ansibleOutput).replace("!", '')
        ansibleOutput = str(ansibleOutput).replace("(", '')
        ansibleOutput = str(ansibleOutput).replace(")", '')
        ansibleOutput = str(ansibleOutput).replace("\\", '')
        ansibleOutput = str(ansibleOutput).replace("/", '')
        ansibleOutput = str(ansibleOutput).replace("sed", '')
        ansibleOutput = str(ansibleOutput).replace("grep", '')
        ansibleOutput = str(ansibleOutput).replace("|", '')


        if "runpipeline" in DevOpsPipelineActions and PipelineName == "" :
            fetchOutput = ""
            if "failed=0" in str(ansibleOutput) and "unreachable=0" in str(ansibleOutput) :
                msg = "Devops Pipeline is found for project - "+devopsProject
            else :
                msg = "Failed to find Devops Pipeline for project - "+devopsProject+" check console logs for debugging"

            my_output_list = ansibleOutput.split('\n')
            for eachword in my_output_list :            
                if "fetchPipelineOut.stdout: " in str(my_output_list) :
                    fetchOutput = str(str(str(my_output_list).split("fetchPipelineOut.stdout: ")[1]).split("',")[0])

            print (fetchOutput)
            dataout["msg"] = msg
            dataout["ansibleOutput"] = str(ansibleOutput)
            dataout["pipelineList"] = str(fetchOutput)


        if "runpipeline" in DevOpsPipelineActions and PipelineName != "" :
            fetchOutput = ""
            if "failed=0" in str(ansibleOutput) and "unreachable=0" in str(ansibleOutput) :
                msg = "Devops Pipeline ran fine for project - "+devopsProject
            else :
                msg = "Failed to run Devops Pipeline for project - "+devopsProject+" check console logs for debugging"

            my_output_list = ansibleOutput.split('\n')
            for eachword in my_output_list :
                if "runPipelineOut.stdout: " in str(my_output_list) :
                    fetchOutput = str(str(str(my_output_list).split("runPipelineOut.stdout: ")[1]).split("',")[0])

            print (fetchOutput)
            dataout["msg"] = msg + " " + fetchOutput
            dataout["ansibleOutput"] = str(ansibleOutput)
            dataout["pipelineList"] = PipelineName


        if "deletepipeline" in DevOpsPipelineActions and PipelineName == "" :
            fetchOutput = ""
            if "failed=0" in str(ansibleOutput) and "unreachable=0" in str(ansibleOutput) :
                msg = "Devops Pipeline found for project - "+devopsProject
            else :
                msg = "Failed to find Devops Pipeline for project - "+devopsProject+" check console logs for debugging"

            my_output_list = ansibleOutput.split('\n')
            for eachword in my_output_list :
                if "fetchPipelineOut.stdout: " in str(my_output_list) :
                    fetchOutput = str(str(str(my_output_list).split("fetchPipelineOut.stdout: ")[1]).split("',")[0])

            print (fetchOutput)
            dataout["msg"] = msg
            dataout["ansibleOutput"] = str(ansibleOutput)
            dataout["pipelineList"] = fetchOutput



        if "deletepipeline" in DevOpsPipelineActions and PipelineName != "" :
            fetchOutput = ""
            if "failed=0" in str(ansibleOutput) and "unreachable=0" in str(ansibleOutput) :
                msg = "Devops Pipeline is deleted for project - "+devopsProject
            else :
                msg = "Failed to delete Devops Pipeline for project - "+devopsProject+" check console logs for debugging"

            my_output_list = ansibleOutput.split('\n')
            for eachword in my_output_list :
                if "deletePipelineOut.stdout: " in str(my_output_list) :
                    fetchOutput = str(str(str(my_output_list).split("deletePipelineOut.stdout: ")[1]).split("',")[0])

            print (fetchOutput)
            dataout["msg"] = msg + " " + fetchOutput
            dataout["ansibleOutput"] = str(ansibleOutput)
            dataout["pipelineList"] = PipelineName



        if "updatepipeline" in DevOpsPipelineActions and PipelineName == "" :
            fetchOutput = ""
            if "failed=0" in str(ansibleOutput) and "unreachable=0" in str(ansibleOutput) :
                msg = "Devops Pipeline found for project - "+devopsProject
            else :
                msg = "Failed to find Devops Pipeline for project - "+devopsProject+" check console logs for debugging"

            my_output_list = ansibleOutput.split('\n')
            for eachword in my_output_list :
                if "fetchPipelineOut.stdout: " in str(my_output_list) :
                    fetchOutput = str(str(str(my_output_list).split("fetchPipelineOut.stdout: ")[1]).split("',")[0])

            print (fetchOutput)
            dataout["msg"] = msg
            dataout["ansibleOutput"] = str(ansibleOutput)
            dataout["pipelineList"] = fetchOutput


        if "updatepipeline" in DevOpsPipelineActions and PipelineName != "" :
            fetchOutput = ""
            if "failed=0" in str(ansibleOutput) and "unreachable=0" in str(ansibleOutput) :
                msg = "Devops Pipeline is update for project - "+devopsProject
            else :
                msg = "Failed to update Devops Pipeline for project - "+devopsProject+" check console logs for debugging"

            my_output_list = ansibleOutput.split('\n')
            for eachword in my_output_list :
                if "updatePipelineOut.stdout: " in str(my_output_list) :
                    fetchOutput = str(str(str(my_output_list).split("updatePipelineOut.stdout: ")[1]).split("',")[0])

            print (fetchOutput)
            dataout["msg"] = msg + " " + fetchOutput
            dataout["ansibleOutput"] = str(ansibleOutput)
            dataout["pipelineList"] = PipelineName



        return jsonify(dataout)
        #return render_template('index.html', msg = msg, user=session["user"], ansibleOutput = ansibleOutput, organization=orgName, PipelineName=PipelineName, Repository=Repository)

      except Exception as e:
        if "createpipeline" in DevOpsPipelineActions :
            dataout["msg"] = str(e)
            dataout["ansibleOutput"] = str(e)

        if "runpipeline" in DevOpsPipelineActions or "updatepipeline" in DevOpsPipelineActions or "deletepipeline" in DevOpsPipelineActions :
            dataout["msg"] = str(e)
            dataout["ansibleOutput"] = str(e)
            pipelineList = "Exception occured"
            dataout["pipelineList"] = pipelineList

        return jsonify(dataout)
        #return render_template('index.html', msg = msg, user=session["user"], ansibleOutput = str(e), organization=orgName, PipelineName=PipelineName, Repository=Repository)



@app.route("/generateAzurePipelineTemplate")
def generateAzurePipelineTemplate() :
    data = ""
    if request.args.get("projType") == "dotnetcore" :
        with open('./azurePipelinesTemplates/azure-pipelines-dotnetcore.yml', 'r') as fh :
            data = yaml.safe_load(fh)

    if request.args.get("projType") == "java" :
        with open('./azurePipelinesTemplates/azure-pipelines-dotnetcore.yml', 'r') as fh :
            data = yaml.safe_load(fh)

    if request.args.get("projType") == "python" :
        with open('./azurePipelinesTemplates/azure-pipelines-dotnetcore.yml', 'r') as fh :
            data = yaml.safe_load(fh)

    ydump = yaml.safe_dump(data, default_flow_style=False, sort_keys=False)
    return Response(ydump, mimetype='text/plain')




def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))

########### New method
def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

if __name__ == "__main__":
    app.run()

