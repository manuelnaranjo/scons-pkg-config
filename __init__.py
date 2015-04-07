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

def exists(env):
    # we suppose the tool is always available
    return True

def PkgConfigSupported(context, version=None):
    if version is None:
        version = '0.25'
    context.Message('Checking for pkg-config with version >= %s...' % version)
    instruction = 'pkg-config --atleast-pkgconfig-version=%s' % version
    ret = context.TryAction(instruction)[0]
    context.Result(ret)
    return ret

def PkgConfigCheck(context, name):
    context.Message('Checking for %s...' % name)
    ret = context.TryAction('pkg-config --exists \'%s\'' % name)[0]
    context.Result(ret)
    return ret

def generate(env):
    from SCons import SConf
    SConfBase = SConf.SConfBase

    class PkgSConfBase(SConfBase):
        def __init__(self, env, custom_tests = {}, *a, **kw):
            pkg_tests = {
                'PkgConfigSupported': PkgConfigSupported,
                'PkgConfigCheck': PkgConfigCheck
            }
            pkg_tests.update(custom_tests)
            SConfBase.__init__(self, env, pkg_tests, *a, **kw)

    setattr(SConf, 'SConfBase', PkgSConfBase)
