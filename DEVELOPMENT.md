## IDE Setup
While application dependencies are built into the container image via the Dockerfile, this doesn't help with IDE features like autocomplete, etc. unless we can tell the IDE to use the same python interpreter.

Several popular IDEs support a way to do this, first just pull the image (or build it locally):

```
docker pull benoverholts/tuner
```

Then you can add the container's Python interpreter to your IDE:
* [IntelliJ instructions](https://www.jetbrains.com/help/idea/configuring-remote-python-sdks.html)
* [VSCode instructions](https://code.visualstudio.com/docs/remote/containers)

## Build and Run

Set up a run configuration in the IDE of your choice or just use the command line. Refer to the following example:

```bash
docker rm -f tuner 2> /dev/null; docker build -t benoverholts/tuner . && docker run \
  --env TZ=America/Los_Angeles \
  --name tuner \
  -v $(pwd)/configuration:/configuration \
  -v /tmp:/output \
  benoverholts/tuner \
  -c configuration/example.yaml -v
```
