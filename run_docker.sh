#!/bin/bash
sudo docker run -v $PWD:/usr/src/app -it \
    -u $(id -u) \
    -e "DISPLAY" \
    -v /etc/group:/etc/group:ro  \
    -v /etc/passwd:/etc/passwd:ro  \
    -v /etc/shadow:/etc/shadow:ro \
    -v /etc/sudoers.d:/etc/sudoers.d:ro \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    ml:2 bash
