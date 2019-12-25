### About

Tuner is a tool designed for home media servers to schedule recording of audio streams and store recordings to a managed location.

### Install
```
docker pull benoverholts/tuner
```


### Configure
Audio **sources** are configured via a YAML file with the following options:

- `id` - unique identifier of a particular show (recommend sequential integers but any string works).
- `name` - name of the program or recording source.
- `url` - source url for audio stream.
- `format` - audio format (supported: `mp3`).
- `start_time_cron` - cron expression describing the desired recording schedule.
- `duration_minutes` - recording duration in minutes.
- `path_template` - template string describing output path rooted at container `/output`. Supports [strftime](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) substitution.

See [configuration/example.yaml](https://github.com/overholts/tuner/blob/master/configuration/example.yaml) for an sample.

### Run

#### Docker-compose Example

A couple of notes:
- The value of `TZ` should match the host machine timezone.
- The arguments to `user` (this is optional) can be used to run as a dedicated system user on the host machine, configure the output file ownership to be readable by a different media server system user, etc.

```
version: '3.7'

services:
  tuner:
    container_name: tuner
    command: -c /configuration/tuner-config.yaml -v
    environment:
      TZ: Etc/UTC
    image: benoverholts/tuner
    user: <UID>:<GID>
    restart: unless-stopped
    volumes:
      - /opt/tuner/configuration/:/configuration
      - /media/music:/output
```

```
docker-compose up -d tuner
```
