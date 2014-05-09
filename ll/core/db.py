# This file is part of Living Labs Challenge, see http://living-labs.net.
#
# Living Labs Challenge is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Living Labs Challenge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Living Labs Challenge. If not, see <http://www.gnu.org/licenses/>.

from pymongo import MongoClient


class CoreDatabase(object):
    def __init__(self):
        self.db = None

    def __getattr__(self, name):
        return self.db.__getattr__(name)

    def init_db(self, db_name, user=None, password=None):
        if self.db == None:
            client = MongoClient()
            self.db = client[db_name]
            if user or password:
                self.db.authenticate(user, password)

db = CoreDatabase()
