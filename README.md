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

## PkgConfigSupported
