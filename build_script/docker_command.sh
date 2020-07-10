#!/usr/bin/env bash

function build_docker(){
    echo "BUILD SEARCH COMPANY by tag(${TAG})"
    docker build -f dockerfile_base --tag search_company:${TAG} ..
}

function run_docker(){
    echo "RUN SEARCH COMPANY by tag(${TAG})"
    docker run -d -p 5000:5000 search_company:${TAG}
}

COMMAND_TYPE=$1
TAG=$2
# No args or '-help' : help message
if [[ $# -lt 2 ]] || [[ ${COMMAND_TYPE} = --help ]] ; then
    echo "Build docker image. "
    echo "------------------------------------------"
    echo "$ docker_command.sh \$1 \$2"
    echo "------------------------------------------"
    echo "\$1: command type(build, run)"
    echo "\$2: docker image tag"
    echo "------------------------------------------"
    exit 0
fi

if [[ ${COMMAND_TYPE} == "build" ]] ; then
    build_docker ${TAG}
elif [[ ${COMMAND_TYPE} == "run" ]] ; then
    run_docker ${TAG}
else
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    echo "'${COMMAND_TYPE}' is not a command."
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    ./docker_command.sh --help
fi