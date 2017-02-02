#!/bin/bash
kill -9 $(lsof -i:6633) 2> /dev/null
kill -9 $(lsof -i:9000) 2> /dev/null
sudo mn -c
