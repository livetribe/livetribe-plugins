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

def load(namespace, subclass=None, recurse=False):
    if subclass:
        instance = subclass()
        instance.Z()
    return set([])


def collect_plugin_modules(namespace, recurse):
    for filepath in collect_plugin_paths(namespace, recurse):
        path_segments = list(filepath.split(os.path.sep))
        path_segments = [p for p in path_segments if p]
        path_segments[-1] = os.path.splitext(path_segments[-1])[0]
        import_path = '.'.join(path_segments)

        try:
            module = import_module(import_path)
        except ImportError:
            module = None

        if module is not None:
            yield module


def collect_plugin_paths(namespace, recurse, already_seen=None):
    already_seen = set() if already_seen is None else already_seen

    # Look in each location in the path
    for path in sys.path:
        # Within this, we want to look for a package for the namespace
        namespace_rel_path = namespace.replace(".", os.path.sep)
        namespace_path = os.path.join(path, namespace_rel_path)
        if os.path.exists(namespace_path):
            for candidate in os.listdir(namespace_path):
                candidate_path = os.path.join(namespace_path, candidate)
                if os.path.isdir(candidate_path):
                    if not is_package(candidate_path):
                        continue
                    if recurse:
                        subns = '.'.join((namespace, candidate.split('.py')[0]))
                        for path in collect_plugin_paths(subns, recurse, already_seen):
                            yield path
                    base = candidate
                else:
                    base, ext = os.path.splitext(candidate)
                    if base == '__init__' or ext != '.py':
                        continue

                candidate_namespace = os.path.join(namespace, candidate)
                if candidate_namespace not in already_seen:
                    already_seen.add(candidate_namespace)
                    yield candidate_namespace


def is_package(path):
    return os.path.exists(os.path.join(path, '__init__.py'))
