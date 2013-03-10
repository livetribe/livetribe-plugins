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

from livetribe.plugins import _is_package, _collect_plugin_paths, collect_plugin_modules, collect_plugin_classes


sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

def test_collect_plugin_classes():
    from acme.plugins import Factory

    results = set()
    for plugin in collect_plugin_classes('acme.plugins', subclasses_of=Factory, recurse=True):
        instance = plugin()
        results.add(instance.work())

    assert len(results) == 2
    assert 'acme.plugins.mock.factory' in results
    assert 'acme.plugins.mock.submodule.factory' in results


def test_collect_plugin_modules():
    from acme.plugins import Factory

    already_seen = set()
    for module in collect_plugin_modules('acme.plugins', recurse=True):
        assert module not in already_seen
        assert isinstance(module, ModuleType)
        already_seen.add(module)

    assert len(already_seen) == 4

    for module in collect_plugin_modules('acme.plugins', recurse=True, methods=['do']):
        result = module.do(45).split(':')
        module_name = result[0]
        value = result[1]
        assert module_name.startswith('acme.plugins')
        assert value == '45'

    modules = [module for module in collect_plugin_modules('acme.plugins')]
    assert len(modules) == 1
    module = modules[0]
    assert module in already_seen
    assert isinstance(module, ModuleType)

    result = module.do(45).split(':')
    module_name = result[0]
    value = result[1]
    assert module_name == 'acme.plugins.mock'
    assert value == '45'


def test_collect_plugin_paths():
    already_seen = set()
    for path in _collect_plugin_paths('acme.plugins', True):
        assert path not in already_seen
        already_seen.add(path)

    assert len(already_seen) == 4
    assert 'acme.plugins/mock' in already_seen
    assert 'acme.plugins.mock/factory.py' in already_seen
    assert 'acme.plugins.mock/submodule' in already_seen
    assert 'acme.plugins.mock.submodule/factory.py' in already_seen

    already_seen = set()
    for path in _collect_plugin_paths('acme.plugins', False):
        assert path not in already_seen
        already_seen.add(path)

    assert len(already_seen) == 1
    assert 'acme.plugins/mock' in already_seen


def test_package():
    assert _is_package(os.path.join(os.path.dirname(__file__), 'data/acme'))
