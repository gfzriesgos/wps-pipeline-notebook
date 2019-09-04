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
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
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

There is an error on importing basemap from within the jupyter notebook.
But once the code runs inside of a python3 console, the import works.
