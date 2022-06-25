#!/bin/sh
operation_content=`cat $1`
python -m authorizator "$operation_content"
