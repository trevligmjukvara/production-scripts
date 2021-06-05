#!/bin/bash
docker run -v $PWD/:/tm:rw --rm trevligmjukvara/production $1
