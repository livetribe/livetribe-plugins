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
from logging import getLogger
import os
import sys

from importlib import import_module


log = getLogger(__name__)

def instantiate_plugin_classes(plugin_classes, *args, **kwargs):
    """A generator function to instantiate plugin instances given a collection of plugin classes.

    :Parameters:
      - `plugin_classes`: a collection of plugin Python classes
      - `args`: arguments to pass to the constructor
      - `kwargs`: keyword arguments to pass to the constructor

The generator function can be used to instantiate plugin classes in a given collection with the same parameters.

::

    from livetribe.plugins import collect_plugin_classes, instantiate_plugin_classes
    from acme.framework import Factory

    plugin_classes = collect_plugin_classes('acme.plugins', subclasses_of=Factory, recurse=True)
    for instance in instantiate_plugin_classes(plugin_classes, 2, 'test', done=False):
        instance.work()

Otherwise, one can instantiate the plugin instances on an individual basis.

::

    from livetribe.plugins import collect_plugin_classes
    from acme.framework import Factory

    plugin_classes = collect_plugin_classes('acme.plugins', subclasses_of=Factory, recurse=True)
    for precedence, plugin in zip(range(len(plugin_classes), plugin_classes):
        instance = plugin(precedence, 'test', done=False)
        instance.work()
   """
    for plugin_class in plugin_classes:
        yield plugin_class(*args, **kwargs)


def collect_plugin_classes(namespace, subclasses_of=None, recurse=False):
    """A generator function that searches namespaces for plugin classes.

    :param namespace: the root namespace to begin searching
    :param subclasses_of: the parent class or classes that plugin classes must be children of
    :type subclasses_of: a single parent class or collection of classes, default None
    :param recurse: whether or not to recurse from the root namespace
    :type recurse: default False
    :rtype: plugin classes that have been found beneath the indicated namespace

    """
    if subclasses_of is not None:
        try:
            subclasses_of = tuple([subclass for subclass in subclasses_of])
        except TypeError:
            subclasses_of = (subclasses_of, )

    for cls in _collect_plugin_named_attributes(namespace, recurse=recurse):
        if isinstance(cls, type):
            if subclasses_of is None:
                yield cls
            elif issubclass(cls, subclasses_of) and not cls in subclasses_of:
                yield cls


def _collect_plugin_named_attributes(namespace, recurse=False):
    for module in collect_plugin_modules(namespace, recurse=recurse):
        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                yield getattr(module, attr_name)


def collect_plugin_modules(namespace, methods=None, recurse=False):
    """A generator function that searches namespaces for plugin methods.

    :param namespace: the root namespace to begin searching
    :param methods: the method name or names that are to be collected
    :type methods: a single method name or collection of names, default None
    :param recurse: whether or not to recurse from the root namespace
    :type recurse: default False
    :rtype: Python methods that have been found beneath the indicated namespace

    """
    if methods:
        try:
            methods = set([method_name for method_name in methods])
        except TypeError:
            methods = set([methods])

    for filepath in _collect_plugin_paths(namespace, recurse):
        path_segments = list(filepath.split(os.path.sep))
        path_segments = [p for p in path_segments if p]
        path_segments[-1] = os.path.splitext(path_segments[-1])[0]
        import_path = '.'.join(path_segments)

        try:
            log.debug('Importing %s', import_path)
            module = import_module(import_path)
            if methods and all(getattr(module, method_name, None) is None for method_name in methods):
                continue
        except ImportError as ie:
            log.warn('Problems importing %s', import_path)
            log.debug('', exc_info=1)
            module = None

        if module is not None:
            yield module


def _collect_plugin_paths(namespace, recurse=False, already_seen=None):
    log.debug('collecting plugin paths for %s%s', namespace, ', recursing modules' if recurse else '')
    already_seen = set() if already_seen is None else already_seen

    # Look in each location in the path
    for sys_path in sys.path:
        # Within this, we want to look for a package for the namespace
        namespace_rel_path = namespace.replace(".", os.path.sep)
        namespace_path = os.path.join(sys_path, namespace_rel_path)
        if os.path.exists(namespace_path):
            for candidate in os.listdir(namespace_path):
                candidate_path = os.path.join(namespace_path, candidate)
                if os.path.isdir(candidate_path):
                    if not _is_package(candidate_path):
                        continue
                    if recurse:
                        subns = '.'.join((namespace, candidate.split('.py')[0]))
                        for path in _collect_plugin_paths(subns, recurse, already_seen):
                            yield path
                else:
                    base, ext = os.path.splitext(candidate)
                    if base == '__init__' or ext != '.py':
                        continue

                candidate_namespace = os.path.join(namespace, candidate)
                if candidate_namespace not in already_seen:
                    already_seen.add(candidate_namespace)
                    yield candidate_namespace


def _is_package(path):
    return os.path.exists(os.path.join(path, '__init__.py'))
