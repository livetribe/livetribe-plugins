Frequently Asked Questions
==========================

.. contents::

Is LiveTribe Plugins thread-safe?
-----------------------

LiveTribe Plugins is thread-safe.

When I collect plugins in :samp:`acme.plugins`, why do functions and classes in the module :samp:`acme.plugins` not picked up?
-----------------------

The plugins framework does not search for functions and classes in the top
level namespace, e.g. :samp:`acme.plugins`, because of the way appending
modules to a given namespace in Python requires that every plugin developer
follow the steps outlined in

http://stackoverflow.com/questions/1675734/how-do-i-create-a-namespace-package-in-python

Such a situation is very brittle and there is no real need to force plugin
developers to place their module functions and classes in the top level
namespace.
