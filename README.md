# bloopslap

A shitty soundboard for the CCC Camp 2023 Flow3r badge.

## Samples

The app uses wav files as samples with a maximum of 10 samples. They are loaded
from the badge flash's rom from `/flash/sys/samples`. Note that the application
does not verify if a file is a valid wav file so it may crash :-)

Converting mp3 to samples can be done with ffmpeg:

```
ffmpeg -i honk.mp3 honk.wav
```
