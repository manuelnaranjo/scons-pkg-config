# -*- coding: utf-8 -*-

# A SCons tool to simplify pkg-config usage on SCons
#
# Copyright (c) 2015 Naranjo Manuel Francisco < naranjo dot manuel at gmail dot com >
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from functools import partial

def exists(env):
    # we suppose the tool is always available
    return True

def PkgConfigSupported(context, version=None):
    if version is None:
        version = '0.25'
    text = 'Checking for ${PKGCONFIG_BIN} with version >= %s...' % version
    instruction = '${PKGCONFIG_BIN} --atleast-pkgconfig-version=%s' % version

    context.Message(context.env.subst(text))
    ret = context.TryAction(instruction)[0]
    context.Result(ret == 1)
    return ret == 1

def PkgConfigCheck(context, name):
    context.Message('Checking for %s...' % name)
    ret = context.TryAction('${PKGCONFIG_BIN} --exists \'%s\'' % name)[0]
    context.Result(ret)
    return ret

def ParseFlags(out, env, cmd):
    out.update(env.ParseFlags(cmd))
    for key, val in list(out.iteritems()):
        if len(out[key]) == 0:
            out.pop(key)

def PkgConfigGetLibs(env, name):
    out = dict()
    env.ParseConfig('pkg-config --libs %s' % name, partial(ParseFlags, out))
    return out

def PkgConfigGetCflags(env, name):
    out = dict()
    env.ParseConfig('pkg-config --cflags %s' % name, partial(ParseFlags, out))
    return out

def PkgConfigGetAllFlags(env, name):
    out = dict()
    env.ParseConfig('pkg-config --libs --cflags %s' % name,
                    partial(ParseFlags, out))
    return out


def generate(env):
    from SCons import SConf
    SConfBase = SConf.SConfBase

    if not env.has_key('PKGCONFIG_BIN'):
        env['PKGCONFIG_BIN'] = 'pkg-config'

    class PkgSConfBase(SConfBase):
        def __init__(self, env, custom_tests = {}, *a, **kw):
            pkg_tests = {
                'PkgConfigSupported': PkgConfigSupported,
                'PkgConfigCheck': PkgConfigCheck
            }
            pkg_tests.update(custom_tests)
            SConfBase.__init__(self, env, pkg_tests, *a, **kw)

    setattr(SConf, 'SConfBase', PkgSConfBase)
    env.AddMethod(PkgConfigGetLibs)
    env.AddMethod(PkgConfigGetCflags)
    env.AddMethod(PkgConfigGetAllFlags)
