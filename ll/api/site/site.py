from flask.ext.restful import Resource, abort
from .. import core

class SiteResource(Resource):
    def check_fields(self, o, fields):
        for f in fields:
            if f not in o:
                abort(400, message="Please specify field '%s'." % f)

    def trycall(self, function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception, e:
            abort(400, message=str(e))

    def get_site_id(self, key):
        user = self.trycall(core.user.get_user, key)
        if not user:
            abort(403, message="No such key.")
        if not user["is_site"]:
            abort(403, message="Not a site. Please use the participant api instead.")
        return user["site_id"]


