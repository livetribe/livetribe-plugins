"""
 Copyright 2013 the original author or authors

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
"""
import os
import sys
from types import ModuleType

from livetribe.plugins import load, is_package, collect_plugin_paths, collect_plugin_modules


sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

def test_load():
    from acme.plugins import Factory


    plugins = load('acme.plugins.mock', subclass=Factory, recurse=True)


def test_collect_plugin_modules():
    already_seen = set()
    for module in collect_plugin_modules('acme.plugins', True):
        assert module not in already_seen
        assert isinstance(module, ModuleType)
        already_seen.add(module)
        module.do(45)


def test_collect_plugin_paths():
    already_seen = set()
    for path in collect_plugin_paths('acme.plugins', True):
        assert path not in already_seen
        already_seen.add(path)


def test_package():
    assert is_package(os.path.join(os.path.dirname(__file__), 'data/acme'))
