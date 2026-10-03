# ODK wrapper scripts

This directory contains wrapper scripts used to invoke ODK workflows through
Docker.

As a general rule, the use of those scripts is not recommended. The [ODK
Runner](https://github.com/INCATools/odkrunner) is the preferred way of
invoking the ODK.

* `odk.sh`: “Generic” wrapper script, basically a stripped down version of the
  `run.sh` script installed with every ODK-seeded repository.
* `seed-via-docker.sh`: Seeding script, for when no pre-existing `run.sh` is
  available (use `odkrun seed` instead).
* `seed-via-docker.bat`: Same, but for Windows.
