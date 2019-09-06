# wps-pipeline-notebook

This is the example notebook to access the wps services of the gfz riesgos server.

Our aim is to provide:
- example code on how to use the service from python
- example code to work with the output of the services
- give people the option to interactivly play around with the parameters for the processes
- test the services
- extract the code to provide a library to use our web services and work
  them in the scientific python ecosystem.

## Requirements

This is a python3 project. It is tested with Python 3.6.8 and with an virtual environment.

To download the necessary python packages you can use the requirements.txt file.

```shell
python3 -m venv wps-pipeline-notebook
source wps-pipeline-notebook/bin/activate
pip3 install -r requirements.txt
ipython3 kernel install --user --name=wps-pipeline-notebook
```

It can be that you also have to install the basemap package yourself:

```
pip3 install -U git+https://github.com/matplotlib/basemap.git 
```

(There can be some issues with the version of matplotlib and basemap, see:
https://github.com/matplotlib/basemap/issues/439).

## Start

You can run the python notebook with
```
jupyter notebook
```

## Known issues

The deus process doesn't work at the moment with the inputs from
the other services.
This has two reasons:
- First the names in the assetmaster and modelprop outputs for
  the taxonomies doesn't match. This is more a problem with those
  services.
- Second deus seems to have a problem with the given shakemap
  from the notebook. We must spend more time to look up what
  the reason for this behaviour is.

## Where does the code comes from?

This repository strongly reuses code that was used in the libraries of the wps services themselves
(most of them are implemented using python).

So we reuse code from:
- https://github.com/gfzriesgos/quakeledger
- https://github.com/gfzriesgos/shakyground

However as we want to provide a library for the format conversions only (so that other people can use the 
wps versions) we may remove the conversion code later from the repositories mentioned above (so that they use
our conversion library instead).


