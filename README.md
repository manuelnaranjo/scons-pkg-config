# About

This is a [SCons](http://www.scons.org) tool that helps working with
pkg-config if the host os supports it.

# Installation

You will need to clone this Git repository and then possibly additionally
provide some links. SCons has a number of ways of adding new tools depending
on whether you want them available only for a single project, for all the
projects of an individual user, or for all projects on a given system. The
location to which the clone should be made depends on which of these
situations you want to support.

Whichever location you choose the command will be:

    $ git clone https://github.com/manuelnaranjo/scons-pkg-config.git pkg-config

The name of the target directory will become the name of the tool for your
situation. In this case _pkg-config_ is the target directory name and hence
_pkg-config_ will be the name of the tool.

# Usage

Currently there are a few methods provided by this tool, in any case you first
need to initialize the tool

    e = Environment(tools=['pkg-config'])

Another alternative is

    e = Environment(...)
    ...
    e.Tool('pkg-config')

Now you you will find two new methods in the Configure environment:
_PkgConfigSupported_ and _PkgConfigCheck_, also three methods are provided in
the caller environment _PkgConfigGetLibs_, _PkgConfigGetCflags_ and
_PkgConfigGetAllFlags_.

## Configure methods

### PkgConfigSupported

This method allows testing if pkg-config is supported in the current
environment, by default it will check for 0.25 as minimun version, but you can
override this value by passing an argument

    e = Environment(tools=['pkg-config'])
    c = e.Configure()
    if c.PkgConfigSupported():
        print 'pkg-config supported'
    ...
    c.Finish()

### PkgConfigCheck

This method checks if a library is provided by pkg-config by warping the
--exists method.

    ...
    if c.PkgConfigCheck('libusb-1.0'):
        print 'libusb-1.0 provided'
    ...

### PkgConfigGetLibs

This method allows to get the flags related to library by wrapping pkg-config
--libs.

    ...
    # the environment will get modified with the flags provided by pkg-config
    e.PkgConfigGetLibs('libusb-1.0')

    # if you don't want the calling environment to be modify you can do this
    flags = e.PkgConfigGetLibs('libusb-1.0', modifyenv=False)
    # now flags is a dictionary with the parsed flags
    e.AppendUnique(**flags)
    ...

### PkgConfigGetCflags

This method allows to get the flags related to c/c++ compiler by wrapping
pkg-config --cflgas.

    ...
    # the environment will get modified with the flags provided by pkg-config
    e.PkgConfigGetCflags('libusb-1.0')

    # if you don't want the calling environment to be modify you can do this
    flags = e.PkgConfigGetCflags('libusb-1.0', modifyenv=False)
    ...

### PkgConfigGetCflags

This method allows to get the flags provided by --libs and --cflags in one call.

    ...
    # the environment will get modified with the flags provided by pkg-config
    e.PkgConfigGetAllFlags('libusb-1.0')

    # if you don't want the calling environment to be modify you can do this
    flags = e.PkgConfigGetAllFlags('libusb-1.0', modifyenv=False)
    ...



## Cross-compiling

Cross-compiling hasn't been tested yet, but an environment variable has been
defined to allow the user of the tool to specify the name of the pkg-config
tool to use, set variable _PPKCONFIG\_BIN_ to the desired value.
