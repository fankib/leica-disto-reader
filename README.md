# Leica Disto Reader

Python script to read out distance measurements of your Leica Disto D1 distance laser measurement device.

Types the distance to any application in mm by a virtual keyboard.

Tested on
  * Leica Disto D1

## RUN

Invoke `python disto_discover.py [--client FD:33:8C:36:69:E5]` to connect with the device and read out the measurements.

### Command Line Arguments

  * [client]: the BLE client MAC Address to connect

## Install

You can run the script directly. I prefer to work in virtual environments.

### Virtual Environment
Create a virtual python environment and install the dependencies in `requirements.txt`.

### Create Alias

Adapt the paths in `leica_disto_reader.sh` and make it executable.

```
chmod u+x leica_disto_reader.sh
```

and add

```
alias leica-disto-reader="/home/benjamin/git/leica-disto-reader/leica_disto_reader.sh"
```

to your `~/.bashrc`.