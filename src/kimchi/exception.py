#
# Kimchi
#
# Copyright IBM Corp, 2013
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import cherrypy
import gettext


from kimchi.i18n import messages as _messages
from kimchi.template import get_lang, validate_language


class KimchiException(Exception):
    def __init__(self, code='', args={}):
        self.code = code

        if cherrypy.request.app:
            msg = self._get_translation(args)
        else:
            msg = _messages.get(code, code) % args

        pattern = "%s: %s" % (code, msg)
        Exception.__init__(self, pattern)

    def _get_translation(self, args):
        lang = validate_language(get_lang())
        paths = cherrypy.request.app.root.paths
        domain = cherrypy.request.app.root.domain
        messages = cherrypy.request.app.root.messages
        text = messages.get(self.code, self.code)

        try:
            translation = gettext.translation(domain, paths.mo_dir, [lang])
        except:
            translation = gettext

        for key, value in args.iteritems():
            if not isinstance(value, unicode):
                args[key] = unicode(value, 'utf-8')

        return unicode(translation.gettext(text), 'utf-8') % args


class NotFoundError(KimchiException):
    pass


class OperationFailed(KimchiException):
    pass


class MissingParameter(KimchiException):
    pass


class InvalidParameter(KimchiException):
    pass


class InvalidOperation(KimchiException):
    pass


class IsoFormatError(KimchiException):
    pass


class TimeoutExpired(KimchiException):
    pass
