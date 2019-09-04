# Contributing to the wps-pipeline-notebook

Please feel free to contribute to the wps-pipeline-notebook.
You can fork it and adopt it as you need (for example to call other web services).

## Version schema
We use a version schema that is just date oriented.

## Branching policy
We use a development branch for every feature that we add.
Master branch should just be used for
a) the initial version
b) the place to merge feature branches into.

## Development
We change the code in this repository as we go to test new services in our
wps pipeline for the RIESGOS project (http://www.riesgos.de/en/).

## Testing
Testing is done using pytest.

## Code styling

For code styling we use pep8 and pylint3.
Make sure that your code is at least compliant with pep8.

There is no need to care about pylint3 warnings regarding to
too less public methods in classes. Those are a good indicator
to use functions / partitial functions instead, but using classes
is clearer in most cases.

Also we don't care about unused arguments once methods implement a
common protocol and those variables are used in other implementations.
