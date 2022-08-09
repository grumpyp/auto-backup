#!/bin/bash

# check OS type - possible extend of executions later


case "$OSTYPE" in
  linux*)   tar -czf $(date +%Y-%m-%d_%H%M%S)_backup.tgz $1 2>/dev/null ;;
  darwin*)  tar -czf $(date +%Y-%m-%d_%H%M%S)_backup.tgz $1 2>/dev/null ;; 
  msys*)    tar -czf $(date +%Y-%m-%d_%H%M%S)_backup.tgz $1 2>/dev/null ;;
esac

echo $(date +%Y-%m-%d_%H%M%S)_backup.tgz created
