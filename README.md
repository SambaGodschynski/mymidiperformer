## Pygame Midi libasound_module_conf_pulse.so error + unable to open slave
### on a Pi4
https://stackoverflow.com/questions/64638256/pygame-midi-libasound-module-conf-pulse-so-error-unable-to-open-slave


```bash
sudo mkdir /usr/lib64/alsa-lib
sudo cp /usr/lib/aarch64-linux-gnu/alsa-lib/* /usr/lib64/alsa-lib/
```

