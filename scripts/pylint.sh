#!/bin/bash

set -o pipefail
set -e

__here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__root="$__here/../"

#------------------------------------------------------------------------------

cd "$__root"

# Run pylint
poetry run pylint ./src
