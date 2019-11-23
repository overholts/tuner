### About

Tuner is a tool designed for home media servers to schedule recording of audio streams and store recordings to a managed location.

```bash
docker build . -t tuner

docker run -it --name tuner --user $(id -u):$(id -g) -e "TZ=America/Los_Angeles" -v /path/to/repo/tuner/configuration/:/configuration -v /tmp/:/output \
  tuner -c /configuration/example.yaml -v
```