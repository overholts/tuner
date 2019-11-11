### About

Tuner is a tool designed for home media servers to schedule recording of audio streams and store recordings to a managed location.

```bash
docker build . -t tuner
docker run -it -e "TZ=America/Los_Angeles" -v /path/to/repo/tuner/configuration/:/configuration tuner -c /configuration/example.yaml
```