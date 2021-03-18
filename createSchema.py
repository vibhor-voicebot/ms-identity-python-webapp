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
def main():

   try:
      #establishing the connection
      #conn = mysql.connector.connect
      conn = pymysql.connect(user='myadmin@azureonboardingdb', password='Feb@2021', host='azureonboardingdb.mysql.database.azure.com', database='defaultdb', ssl= {'ssl': {'ca': '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'}})

      #Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      #Dropping ClientsMappingVault table if already exists.
      cursor.execute("DROP TABLE IF EXISTS ClientsMappingVault")
 
      #Creating table as per requirement1 (hardcoded for now)
      sql ='''CREATE TABLE ClientsMappingVault(
            id int(30) not null auto_increment,
            projectName VARCHAR(100) not null,
            clientID VARCHAR(100)  null,
            clientSecret VARCHAR(100)  null,
            servicePrincipalName VARCHAR(100) null,
            tenantID VARCHAR(100)  null,
            objectID VARCHAR(100)  null,
            orgName VARCHAR(100)  not null,
            resourceGroupName VARCHAR(200)  null,
            devopsOrgName VARCHAR(200) null,
            devopsProject VARCHAR(200) null,
            PAT VARCHAR(200) null,
            GITHUB_PAT VARCHAR(200) null,
            is_onboarded VARCHAR(10) null,
            PRIMARY KEY (id, projectName, orgName)) auto_increment=2'''

      cursor.execute(sql)
      print("table created ClientsMappingVault")
      cursor.execute("DESCRIBE ClientsMappingVault")
      rows = cursor.fetchall()
      print(rows)


      #Dropping RolesMapping table if already exists.
      cursor.execute("DROP TABLE IF EXISTS RolesMapping")

      #Creating table as per requirement1 (hardcoded for now)
      sql1 ='''CREATE TABLE RolesMapping(
            organization VARCHAR(200) null,
            userprincipalname VARCHAR(200) not null,
            role VARCHAR(100)  null,
            PRIMARY KEY (userprincipalname))'''

      cursor.execute(sql1)
      print("table created RolesMapping")
      cursor.execute("DESCRIBE RolesMapping")
      rows1 = cursor.fetchall()
      print(rows1)

       
   except Exception as e :
      print("exception occured while connecting to Azure MySQL", str(e))
      if "Client with IP address " in str(e):
         #attemptThreshold = "3"
         respcommon = exceptionhandler()
   
   finally:
      conn.close()

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
            conn = pymysql.connect(user='myadmin@azureonboardingdb', password='Feb@2021', host='azureonboardingdb.mysql.database.azure.com', database='defaultdb', ssl= {'ssl': {'ca': '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'}})

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

            cmd2 = ['mysql', 'server', 'firewall-rule', 'create', '--resource-group', 'myresourcegroup', '--server', 'azureonboardingdb', '--name', 'AllowIP', '--start-ip-address', '--end-ip-address']

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


if __name__ == "__main__":
   main()
