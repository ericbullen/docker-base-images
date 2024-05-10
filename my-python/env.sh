source ../global.sh

export GOLD_BASE_IMAGE_LATEST=$(cat ../my-goldimage/digests/latest.digest)

CONTAINER_LABEL="app=python,3.11"
