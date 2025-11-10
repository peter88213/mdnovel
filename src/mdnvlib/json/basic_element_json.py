"""Provide a base class for mdnovel element JSON import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class BasicElementJson:

    def import_data(self, element, json):
        element.title = json.get('Title', None)
        element.desc = json.get('Desc', None)
        element.links = json.get('Links', {})

    def export_data(self, element, json):
        if element.title:
            json['Title'] = element.title
        if element.desc:
            json['Desc'] = element.desc
        if element.links:
            json['Links'] = element.links
        return json

