**tl;dr** - clone and change the configuration volume host path below to match repo location.

```bash
docker container rm tuner
docker build . -t tuner
docker run --name tuner --user 993:998 -e "TZ=Etc/UTC" -v /path/to/repo/configuration/:/configuration -v /tmp:/output tuner -c /configuration/example.yaml -v
```