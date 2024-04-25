#!/bin/bash


CONTAINER_ALREADY_STARTED="container-started.txt"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"
    python database.py
else
    echo "-- Not first container startup --"
fi