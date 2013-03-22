#
# Copyright 2013 the original author or authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import os
import sys
from types import ModuleType

from livetribe.plugins import collect_plugin_classes, instantiate_plugin_classes, collect_plugin_modules, _collect_plugin_paths, _is_package


def test_collect_plugin_classes():
    from acme.framework.factory import Factory

    widget = 2
    results = set()
    for plugin_class in collect_plugin_classes('acme.plugins', subclasses_of=Factory, recurse=True):
        plugin = plugin_class(widget, append_widget=True)
        results.add(plugin.work())

    assert len(results) == 2
    assert 'acme.plugins.mock.factory:2' in results
    assert 'acme.plugins.mock.submodule.factory:2' in results


def test_instantiate_plugin_classes():
    from acme.framework.factory import Factory

    widget = 2
    results = set()
    plugin_classes = collect_plugin_classes('acme.plugins', subclasses_of=Factory, recurse=True)
    for plugin in instantiate_plugin_classes(plugin_classes, widget, append_widget=True):
        results.add(plugin.work())

    assert len(results) == 2
    assert 'acme.plugins.mock.factory:2' in results
    assert 'acme.plugins.mock.submodule.factory:2' in results


def test_collect_plugin_modules():
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
    assert _is_package(os.path.join(os.path.dirname(__file__), 'acme'))
