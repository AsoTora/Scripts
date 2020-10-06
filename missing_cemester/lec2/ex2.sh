#!/bin/bash

marco() {
    dir="$(pwd)"
    export dir
}

polo() {
    echo "$dir"     
    cd "$dir" || exit
}

marco
polo
