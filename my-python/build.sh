#!/usr/bin/env -S -i bash

# The above sets up a clean environment so that
# no env vars outside of the env.sh will exist

set -x

[ -r env.sh ] && source env.sh

build
