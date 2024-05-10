source ../global.sh

SHA="sha256:3853398d8cefdc1c02ca82cd809ab3ab3851728da0de68325389b7e53eb26acd"

export UBUNTU_BASE_IMAGE="ubuntu:23.10@${SHA}"

CONTAINER_LABEL="app=ubuntu,23.10"
