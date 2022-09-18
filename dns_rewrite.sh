#!/bin/bash

FILE=${1:-devices.yml}

LIST_OF_FQDNS=$(grep fqdn ${FILE} | awk '{print $3}')

while IFS= read -r fqdn; do
    sed -i "s/${fqdn}/$(host ${fqdn} | awk '{print $4}')/" $FILE
done <<< "$LIST_OF_FQDNS"
