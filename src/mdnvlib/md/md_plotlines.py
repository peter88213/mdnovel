"""Provide a class for Markdown plot line descriptions export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from string import Template

from mdnvlib.md.md_file import MdFile
from mdnvlib.novx_globals import PLOTLINES_SUFFIX
from mdnvlib.novx_globals import SECTIONS_SUFFIX
from mdnvlib.novx_globals import _


class MdPlotlines(MdFile):
    """Markdown plot lines description file representation.

    Export descriptions of plot lines and plot points.
    """
    DESCRIPTION = _('Plot lines')
    SUFFIX = PLOTLINES_SUFFIX

    _fileHeader = f'{MdFile._fileHeader}# {DESCRIPTION}\n\n'
    _arcHeadingTemplate = f'''# {_('Plot lines')}
'''

    _plotLineTemplate = '\n## $Title\n\n$Desc\n\n$TurningPoints\n\n'
    _plotPointTemplate = '### $Title\n\n$Desc'
    _assocSectionTemplate = '$Section: *$SectionTitle*'

    def write(self):
        """Initialize "first plot line" flag.

       Extends the superclass constructor.
        """
        self._firstPlotLine = True
        super().write()

    def _get_plotLineMapping(self, plId):
        """Add associated sections to the plot line mapping dictionary.
        
        Extends the superclass method.
        """
        arcMapping = super()._get_plotLineMapping(plId)
        if self._firstPlotLine:
            arcMapping['Heading'] = self._arcHeadingTemplate
            self._firstPlotLine = False
        else:
            arcMapping['Heading'] = ''
        plotPoints = []
        for ppId in self.novel.tree.get_children(plId):
            plotPointMapping = dict(
                ID=ppId,
                Title=self.novel.plotPoints[ppId].title,
                Desc=self._convert_from_mdnov(self.novel.plotPoints[ppId].desc),
            )
            template = Template(self._plotPointTemplate)
            plotPoints.append(template.safe_substitute(plotPointMapping))
            scId = self.novel.plotPoints[ppId].sectionAssoc
            if scId:
                sectionAssocMapping = dict(
                    SectionTitle=self.novel.sections[scId].title,
                    ProjectName=self._convert_from_mdnov(self.projectName, True),
                    Section=_('Section'),
                    Description=_('Description'),
                    Manuscript=_('Manuscript'),
                    scID=scId,
                    SectionsSuffix=SECTIONS_SUFFIX,
                )
                template = Template(self._assocSectionTemplate)
                plotPoints.append(template.safe_substitute(sectionAssocMapping))
        arcMapping['TurningPoints'] = '\n\n'.join(plotPoints)
        return arcMapping

