import unittest

class TestRetryStdErrorMessage(unittest.TestCase):

    def _getApplication(self):
        from OFS.Application import Application
        app = Application()
        return app

    def _addFolder(self, app):
        from OFS.Folder import manage_addFolder
        manage_addFolder(app, 'folder1')

    def _getTargetClass(self):
        return SimpleItem

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw).__of__(FauxRoot())

    def test_retry_std_error_message(self):

        class REQUEST(object):
            class RESPONSE(object):
                handle_errors = True

        app = self._getApplication()
        self._addFolder(app)

        app.standard_error_message = lambda *args, **kw: 'root error message'

        def _raise_during_standard_error_message(*args, **kw):
            raise ZeroDivisionError('testing')

        app.folder1.standard_error_message = _raise_during_standard_error_message

        t,v,tb = app.folder1.raise_standardErrorMessage(
            error_type=OverflowError,
            error_value=OverflowError('simple'),
            REQUEST = REQUEST()
        )

        exp = 'root error message'

        self.assertEqual(v, exp)
