# MBOPP Stimuli Demo
A simple GUI to demonstrate/explore MBOPP stimuli

See the following for original work:
> Jasmin, K., Dick, F., & Tierney, A. T. (2020). The Multidimensional Battery of Prosody Perception (MBOPP). *Wellcome Open Research*, 5, 4. https://doi.org/10.12688/wellcomeopenres.15607.1

## Acquiring stimuli
To download stimuli, see:
> Jasmin, Kyle and Dick, Frederic and Tierney, Adam (2019): *Multidimensional Battery of Prosody Perception*. Birkbeck College, University of London. doi: https://doi.org/10.18743/DATA.00037

Extract all `.wav` files to to `assets/audio/` with no deeper folders. E.g.:
* `MBOPP/assets/audio/focus20_pitch10_time10.wav`
* `MBOPP/assets/audio/phrase9_pitch70_time70.wav`
* etc.

## Install dependencies
```bash
pipenv install
```

## Execute
```bash
pipenv shell
python -m MBOPP
```
