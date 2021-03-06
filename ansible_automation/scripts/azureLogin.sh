#!/usr/bin/bash
loginOut=""
loginOut=`timeout 40s az login`
#sleep 40s
echo "$loginOut"
