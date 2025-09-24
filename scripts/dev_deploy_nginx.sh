#!/usr/bin/env bash
set -euo pipefail

# Dev Nginx deployment script (Docker) using official envsubst templates.
# Usage examples:
#   ./scripts/dev_deploy_nginx.sh --upstream-host 127.0.0.1 --upstream-port 3000 --host-port 80
#   ./scripts/dev_deploy_nginx.sh -u api.internal -p 8080 -P 80 -n nginx-dev

IMAGE="nginx:alpine"
CONTAINER_NAME="nginx-dev"
UPSTREAM_HOST="127.0.0.1"
UPSTREAM_PORT="3000"
HOST_PORT="8080"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONF_DIR="$REPO_ROOT/ops/nginx"
TEMPLATES_DIR="$CONF_DIR/templates"

usage() {
  echo "Usage: $0 [-n name] [--name name] [-u host] [--upstream-host host] [-p port] [--upstream-port port] [-P hostPort] [--host-port hostPort]" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--name) CONTAINER_NAME="$2"; shift 2;;
    -u|--upstream-host) UPSTREAM_HOST="$2"; shift 2;;
    -p|--upstream-port) UPSTREAM_PORT="$2"; shift 2;;
    -P|--host-port) HOST_PORT="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1;;
  esac
done

echo "[dev-deploy] Image:          $IMAGE"
echo "[dev-deploy] Container name: $CONTAINER_NAME"
echo "[dev-deploy] Upstream:       $UPSTREAM_HOST:$UPSTREAM_PORT"
echo "[dev-deploy] Host port:      $HOST_PORT -> 80"
echo "[dev-deploy] Config dir:     $CONF_DIR"

# Ensure config files exist
if [[ ! -f "$CONF_DIR/nginx.conf" ]]; then
  echo "[dev-deploy] ERROR: Missing $CONF_DIR/nginx.conf" >&2
  exit 1
fi
if [[ ! -f "$TEMPLATES_DIR/default.conf.template" ]]; then
  echo "[dev-deploy] ERROR: Missing $TEMPLATES_DIR/default.conf.template" >&2
  exit 1
fi

# Stop/remove existing container if present
if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
  echo "[dev-deploy] Stopping existing container $CONTAINER_NAME ..."
  docker update --restart=no "$CONTAINER_NAME" || true
  docker stop -t 5 "$CONTAINER_NAME" || true
  docker rm -f "$CONTAINER_NAME" || true
fi

echo "[dev-deploy] Pulling image $IMAGE ..."
docker pull "$IMAGE" >/dev/null

echo "[dev-deploy] Starting $CONTAINER_NAME ..."
docker run -d --name "$CONTAINER_NAME" --restart unless-stopped \
  -e UPSTREAM_HOST="$UPSTREAM_HOST" \
  -e UPSTREAM_PORT="$UPSTREAM_PORT" \
  -p "$HOST_PORT:80" \
  -v "$CONF_DIR/nginx.conf":/etc/nginx/nginx.conf:ro \
  -v "$TEMPLATES_DIR":/etc/nginx/templates:ro \
  "$IMAGE"

echo "[dev-deploy] Validating config ..."
docker exec "$CONTAINER_NAME" nginx -t

echo "[dev-deploy] Recent logs:"
docker logs --tail 50 "$CONTAINER_NAME" || true

echo "[dev-deploy] Running containers:"
docker ps --filter "name=$CONTAINER_NAME"

echo "[dev-deploy] Done. Visit http://localhost:$HOST_PORT/ (or EC2 public IP)."



