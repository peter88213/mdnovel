"""Provide a class for mdnovel element JSON import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.json.basic_element_tags_json import BasicElementTagsJson
from mdnvlib.novx_globals import verified_date
from mdnvlib.novx_globals import verified_int_string
from mdnvlib.novx_globals import verified_time


class SectionJson(BasicElementTagsJson):

    def import_data(self, element, json):
        super().import_data(element, json)

        # Attributes.
        scType = json.get('type', 0)
        if scType in (0, 1, 2, 3):
            element.scType = scType
        else:
            element.scType = 1
        status = json.get('status', 1)
        if status in (1, 2, 3, 4, 5):
            element.status = status
        else:
            element.status = 1
        scene = json.get('scene', 0)
        if scene in (0, 1, 2, 3):
            element.scene = scene
        else:
            element.scene = 0

        element.appendToPrev = json.get('append', False)

        # Text fields.
        element.sectionContent = json.get('Content', None)
        element.goal = json.get('Goal', None)
        element.conflict = json.get('Conflict', None)
        element.outcome = json.get('Outcome', None)

        # Date/Day and Time.
        element.date = verified_date(json.get('Date', None))
        if not element.date:
            element.day = verified_int_string(json.get('Day', None))

        element.time = verified_time(json.get('Time', None))

        # Duration.
        element.lastsDays = verified_int_string(json.get('LastsDays', None))
        element.lastsHours = verified_int_string(json.get('LastsHours', None))
        element.lastsMinutes = verified_int_string(json.get('LastsMinutes', None))

        # Characters references.
        element.characters = json.get('Characters', [])

        # Locations references.
        element.locations = json.get('Locations', [])

        # Items references.
        element.items = json.get('Items', [])

    def export_data(self, element, json):
        json = super().export_data(element, json)
        if element.scType:
            json['type'] = element.scType
        if element.status > 1:
            json['status'] = element.status
        if element.scene > 0:
            json['scene'] = element.scene
        if element.appendToPrev:
            json['append'] = True

        # Text fields.
        if element.sectionContent:
            json['Content'] = element.sectionContent
        if element.goal:
            json['Goal'] = element.goal
        if element.conflict:
            json['Conflict'] = element.conflict
        if element.outcome:
            json['Outcome'] = element.outcome

        # Date/Day and Time.
        if element.date:
            json['Date'] = element.date
        elif element.day:
            json['Day'] = element.day
        if element.time:
            json['Time'] = element.time

        # Duration.
        if element.lastsDays and element.lastsDays != '0':
            json['LastsDays'] = element.lastsDays
        if element.lastsHours and element.lastsHours != '0':
            json['LastsHours'] = element.lastsHours
        if element.lastsMinutes and element.lastsMinutes != '0':
            json['LastsMinutes'] = element.lastsMinutes

        # Characters references.
        if element.characters:
            json['Characters'] = element.characters

        # Locations references.
        if element.locations:
            json['Locations'] = element.locations

        # Items references.
        if element.items:
            json['Items'] = element.items

        return json
