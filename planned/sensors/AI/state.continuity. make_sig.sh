#!/usr/bin/env bash
# Usage: ./make_sig.sh capsule.json
jq 'del(.capsule.hash)' "$1" | sha256sum | cut -c1-20 | xxd -r -p | base32 | cut -c1-12 | tr -d '='
