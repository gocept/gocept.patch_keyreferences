"""Functional tests for zope.app.catalog
"""
from .testing import PatchedAppCatalogLayer
from zope.app.wsgi.testlayer import http as _http
import doctest


def http(query_str, *args, **kwargs):
    wsgi_app = PatchedAppCatalogLayer.make_wsgi_app()
    # Strip leading \n
    query_str = query_str.lstrip()
    kwargs.setdefault('handle_errors', False)
    if not isinstance(query_str, bytes):
        query_str = query_str.encode("utf-8")
    return _http(wsgi_app, query_str, *args, **kwargs)


def test_suite():
    suite = doctest.DocFileSuite(
        'regression.rst',
        globs={
            'http': http,
            'getRootFolder': PatchedAppCatalogLayer.getRootFolder,
        },
        optionflags=(doctest.ELLIPSIS
                     | doctest.NORMALIZE_WHITESPACE),
    )
    suite.layer = PatchedAppCatalogLayer
    return suite
