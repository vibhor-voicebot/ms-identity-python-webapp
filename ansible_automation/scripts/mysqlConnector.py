import mysql
import mysql.connector
import sys, getopt
import pymysql
import subprocess
from subprocess import PIPE, run
import sys,os
from azure.cli.core import get_default_cli
from flask import Flask, jsonify, request, render_template
import socket, os, json, yaml, sys
import requests
import random, os
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
import subprocess

#Use the get_client_from_auth_file method to create the client object:
from azure.common.client_factory import get_client_from_auth_file
from azure.mgmt.resource import SubscriptionClient

############################################################################
# Main handler Method
############################################################################
def main(argv):
   userName = ''
   passCode = ''
   serverName = ''
   dbName = ''
   tableName = ''
   action = ''
   publicKey = ''
   servicePrincipalName = ''
   clientID = ''
   clientSecret = ''
   tenantID = ''
   sObjectID = ''
   uObjectID = ''

   #resource_client = get_client_from_cli_profile(ResourceManagementClient)
   #rg_result = resource_client.resource_groups.create_or_update('RESOURCE_GROUP_NAME',{ "location": "LOCATION" })

   try:
      opts, args = getopt.getopt(argv,"hu:p:s:d:t:a:k:n:c:r:z:o:i:",["uUser=","pPass=","sServer=","dDB=","tTableName=","aAction=","kPublickKey=","nServicePrincipalName=","cClientID=","rClientSecret=","zTenantID=","oSObjectID=","iUObjectID="])
   except getopt.GetoptError:
      print ('test.py -u <user> -p <password> -s <server> -d <dbname> -t <tablename> -a <action>  -k <publickey>, -n <serviceprincipalname>, -c <clientid>, -r <clientsecret>, -z <tenantid>, -o <sobjectid>, -i <uobjectid>')
      sys.exit(6)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py  -u <user> -p <password> -s <server> -d <dbname> -t <tablename> -a <action>  -k <publickey>, -n <serviceprincipalname>, -c <clientid>, -r <clientsecret>, -z <tenantid>, -o <sobjectid>, -i <uobjectid>')
         sys.exit()
      elif opt in ("-u", "--uUser"):
         userName = arg
      elif opt in ("-p", "--pPass"):
         passCode = arg
      elif opt in ("-s", "--sServer"):
         serverName = arg
      elif opt in ("-d", "--dDB"):
         dbName = arg
      elif opt in ("-d", "--tTableName"):
         tableName = arg
      elif opt in ("-d", "--aAction"):
         action = arg
      elif opt in ("-k", "--kPublickKey"):
         publicKey = arg
      elif opt in ("-n", "--nServicePrincipalName"):
         servicePrincipalName = arg
      elif opt in ("-c", "--cClientID"):
         clientID = arg
      elif opt in ("-r", "--rClientSecret"):
         clientSecret = arg
      elif opt in ("-z", "--zTenantID"):
         tenantID = arg
      elif opt in ("-o", "--oSObjectID"):
         sObjectID = arg
      elif opt in ("-i", "--iUObjectID"):
         uObjectID = arg

   print ('Input1 ', userName)
   print ('input2 ', passCode)
   print ('Input3 ', serverName)
   print ('input4 ', dbName)
   print ('Input5 ', tableName)
   print ('input6 ', action)
   print ('Input7 ', publicKey)
   print ('input8 ', servicePrincipalName)
   print ('Input9 ', clientID)
   print ('input10 ', clientSecret)
   print ('Input11 ', tenantID)
   print ('input12 ', sObjectID)
   print ('input13 ', uObjectID)

   respcommon = ""

   try :

      #establishing the connection
      #conn = mysql.connector.connect
      conn = pymysql.connect(user='myadmin@ansibledemoserver', password='Feb@2021', host='ansibledemoserver.mysql.database.azure.com', database='defaultdb', ssl= {'ssl': {'ca': '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'}})

      #Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      #Invoke appropriate func from here :
      if "insert" in action.lower() :
         respcommon = insertRow(tableName, publicKey, servicePrincipalName, clientID, clientSecret, tenantID, sObjectID, uObjectID) 

      if "select" in action.lower() :
         respcommon = fetchRow(tableName, publicKey, servicePrincipalName)

      if "update" in action.lower() :
         respcommon = updateRow(tableName, publicKey, ServicePrincipalName, clientID, clientSecret, tenantID, sObjectID)

   except Exception as e :
      print("exception occured while connecting to Azure MySQL", str(e))
      if "Client with IP address " in str(e):
         #attemptThreshold = "3"
         respcommon = exceptionhandler()
          
   return str(respcommon)


############################################################################
# main exceptional method :
############################################################################
def exceptionhandler():

   passcode = 1111
   attempts = 0
   returnResp = ""
   ipAddressValue = ""
   while passcode == 1111:

      if attempts < 2:
         attempts += 1
         try:
            returnResp = "OK"
            #establishing the connection
            #conn = mysql.connector.connect
            conn = pymysql.connect(user='myadmin@ansibledemoserver', password='Feb@2021', host='ansibledemoserver.mysql.database.azure.com', database='defaultdb', ssl= {'ssl': {'ca': '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'}})

            #Creating a cursor object using the cursor() method
            cursor = conn.cursor()

         except Exception as e :
            print("exception occured while connecting to Azure MySQL", str(e))
            returnResp = "exception occured while connecting to Azure MySQL" + " " + str(e)
            #cmd = 'echo '+str(str(str(e).split("(9000, ")[1]).split(")")[0])+' | awk -F"Client with IP address " \'{print $2}\' | awk -F" " \'{print $1}\' | sed \'s/^ *//;s/ *$//\' | sed "s/\'//g"'
            intmStr = str(str(str(e).split("(9000, ")[1]).split(")")[0]).strip("'").strip(".")
            print (intmStr)
            cmd = "echo "+intmStr+" | grep -o \\'[0-9]*.[0-9]*.[0-9]*.[0-9]*\\' |  sed \"s/'//g\""  
            #cmd = "ls -lrt"
            print (cmd)
            #ipAddrData = subprocess.Popen(subprocess.check_output(["bash", "-c", cmd], stderr=subprocess.STDOUT, shell=True)
            ipAddrData = subprocess.Popen(["bash", "-c", cmd],  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            ipAddressValue = ipAddrData.stdout.read().strip().decode("utf-8")
            print ("ipadress pulled is ",ipAddressValue)
            #cmd2 = "az mysql server firewall-rule create --resource-group myresourcegroup --server ansibledemoserver --name AllowIP --start-ip-address "+str(ipAddrData.stdout.read().strip())+" --end-ip-address "+str(ipAddrData.stdout.read().strip())

            cmd2 = ['mysql', 'server', 'firewall-rule', 'create', '--resource-group', 'myresourcegroup', '--server', 'ansibledemoserver', '--name', 'AllowIP', '--start-ip-address', '--end-ip-address']

            cmd2.insert(11, ipAddressValue)
            cmd2.insert(13, ipAddressValue)
            print ("command is +++++++++++++++++++++++++++")
            print (cmd2)
            get_default_cli().invoke(cmd2)
            
            #p2 = subprocess.Popen(["bash", "-c", cmd2], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            #ipAddrData2 = p2.stdout.read().strip().decode("utf-8")
            #print ("Firewall rule creation output "+ str(response))
      
      else:
         if "OK" != returnResp.upper() :
            returnResp = "All attempts to connect to Azure MySQL DB are failed.."
         exit()

   return str(returnResp)

############################################################################
# Preparing SQL query to INSERT a record into the database.
############################################################################
def insertRow(tablename, publickey, serviceprincipalname, clientid, clientsecret, tenantid, sobjectid, uobjectid) :
   itablename = tablename
   ipublickey = publickey
   iserviceprincipalname = servicepricipalname
   iclientid = clientid
   iclientsecret = clientsecret
   itenantid = tenantid
   isobjectid = sobjectid
   resp = ""

   sql = """INSERT INTO EMPLOYEE(PublicKey, ServicePrincipalName, ClientID, ClientSecret, TenantID, sObjectID, uObjectID)
   VALUES ('Mac', 'Mohan', 20, 'M', 2000, 'M', 'M')"""
   try:
     try:
      # Executing the SQL command
      cursor.execute(sql)

      # Commit your changes in the database
      conn.commit()

     except:
      # Rolling back in case of error
      conn.rollback()
      resp = "exception occured while inserting the row"

     resp = "row inserted successfully"

   finally:   
      # Closing the connection
      conn.close()

   return str(resp)


############################################################################
#Retrieving single row
############################################################################
def fetchRow(tablename, publickey, serviceprincipalname) :
   itablename = tablename
   ipublickey = publickey
   iserviceprincipalname = servicepricipalname

   sql = '''SELECT * from EMPLOYEE'''

   #Executing the query
   cursor.execute(sql)

   #Fetching 1st row from the table
   result = cursor.fetchone();
   print(result)

   #Closing the connection
   conn.close()

   return str(result)


############################################################################
#Preparing the query to update the records
############################################################################
def updateRow(tablename, publickey, serviceprincipalname, clientid, clientsecret, tenantid, sobjectid) :
   itablename = tablename
   ipublickey = publickey
   iserviceprincipalname = servicepricipalname
   iclientid = clientid
   iclientsecret = clientsecret
   itenantid = tenantid
   isobjectid = sobjectid
   resp = ""

   sql = '''UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = 'M' '''
   try:
     try:
      # Execute the SQL command
      cursor.execute(sql)
   
      # Commit your changes in the database
      conn.commit()
     except:
      # Rollback in case there is any error
      conn.rollback()
      resp = "exception occured while updating the row"

     resp = "row updated successfully"

   finally:
      #Closing the connection
      conn.close()

   return str(resp)

if __name__ == "__main__":
   main(sys.argv[1:])
