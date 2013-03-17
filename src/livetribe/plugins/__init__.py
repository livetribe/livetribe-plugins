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
from logging import getLogger
import os
import sys

from importlib import import_module


log = getLogger(__name__)

def instantiate_plugin_classes(plugin_classes, *args, **kwargs):
    """A simple function to instantiate a collection of plugin classes.

   Raises :class:`TypeError` if `name` is not an instance of
   :class:`basestring` (:class:`str` in python 3). Raises
   :class:`~pymongo.errors.InvalidName` if `name` is not a valid
   database name.

   :Parameters:
     - `connection`: a client instance
     - `name`: database name

   """
    for plugin_class in plugin_classes:
        yield plugin_class(*args, **kwargs)


def collect_plugin_classes(namespace, subclasses_of=None, recurse=False):
    """
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


def collect_plugin_modules(namespace, recurse=False, methods=None):
    methods = methods if methods is not None else set()
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
            log.debug(exc_info=1)
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
