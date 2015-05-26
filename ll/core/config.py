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

import datetime

config = {
    "KEY_LENGTH": 32,
    "PASSWORD_LENGHT": 8,
    "EMAIL_FROM": 'challenge@living-labs.net',
    "SEND_EMAIL": False,
    "URL_WEB": "http://doc.living-labs.net/en/latest/guide-participant.html",
    "URL_API": "http://living-labs.net:5000/api",
    "URL_DASHBOARD": "http://living-labs.net:5001",
    "URL_DOC": "http://doc.living-labs.net",
    "URL_GIT": "https://bitbucket.org/living-labs/ll-api/",
    "URL_REGISTRATION_FORM": "http://living-labs.net/wp-content/uploads/2014/06/LLC14-Application-form.pdf",
    "EMAIL_ORGANIZERS": ["krisztian.balog@uis.no",
                         "liadh.kelly@scss.tcd.ie",
                         "anne.schuth@uva.nl"],
    "TEST_DATE": datetime.date(2015, 5, 1),
    "TEST_DATE_END": datetime.date(2015, 5, 16),
}
