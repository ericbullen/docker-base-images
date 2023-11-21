function build() {
	set -e

	IMG_NAME="${CONTAINER_NAME}:${TAG_VERSION}"

	if [ -z "${CONTAINER_LABEL}" ]; then
		CONTAINER_LABEL="1.0.0"
	fi

	[ ! -d digests/ ] && mkdir digests/

	echo "## Rendered Dockerfile for: ${IMG_NAME}"
	cat Dockerfile | ../render.py
	cat Dockerfile | ../render.py | docker build . --network=host --label ${CONTAINER_LABEL} -f - --tag ${IMG_NAME}

	echo "${IMG_NAME}" > digests/latest.digest

	set +e
}

# Sane defaults
export CONTAINER_NAME=$(basename $(pwd))
export TAG_VERSION="1.0.0"

