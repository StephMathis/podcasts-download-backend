#!/bin/bash

ENV=$1

if [ $# -lt 1 ]
then
    echo "Usage: $0 local"
else
    if [[ "test local" =~ "${ENV}" ]]
    then

        echo "Loading ${ENV} environment."

        $(cat ".env-common" ".env-${ENV}" ".env-${ENV}-secret" \
        | sed 's|^|export |')

        echo "Loaded ${ENV} environment."
    fi
fi



