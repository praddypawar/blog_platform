#!/bin/bash
# wait-for-db.sh

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until (echo > /dev/tcp/$host/$port) >/dev/null 2>&1; do
  echo "Waiting for $host:$port to be available..."
  sleep 1
done

echo "$host:$port is available, continuing..."

exec $cmd