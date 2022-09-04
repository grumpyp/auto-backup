#!/bin/bash

# check OS type - possible extend of executions later

timestamp=$(date +%Y-%m-%d_%H%M%S)

case "$OSTYPE" in
  linux*)   tar -czf ${timestamp}_backup.tgz $1 2>/dev/null ;;
  darwin*)  tar -czf ${timestamp}_backup.tgz $1 2>/dev/null ;; 
  msys*)    tar -czf ${timestamp}_backup.tgz $1 2>/dev/null ;;
esac

echo ${timestamp}_backup.tgz created
