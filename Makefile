all: build run

build:
	podman build -t environmental-data-recorder .

run:
	podman run --rm \
	  --network homeautomation \
	  --network isolation \
	  --env-file="${CURDIR}/../coned-usage-visualizer/.credentials.env" \
          --env-file="${CURDIR}/.credentials.env" \
          --dns 8.8.8.8 \
          environmental-data-recorder
