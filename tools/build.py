"""Build the mdnovel release package.

Note: VERSION must be updated manually before starting this script.
        
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

sys.path.insert(0, f'{os.getcwd()}/../../mdnovel/tools')
from package_builder import PackageBuilder

VERSION = '0.3.1'


class ApplicationBuilder(PackageBuilder):

    PRJ_NAME = 'mdnovel'
    GERMAN_TRANSLATION = True

    def __init__(self, version):
        super().__init__(version)
        self.sourceFile = f'{self.sourceDir}{self.PRJ_NAME}_.py'

    def add_extras(self):
        self.add_icons()

    def build_script(self):
        os.makedirs(self.testDir, exist_ok=True)
        self.inline_modules(self.sourceFile, self.testFile, copynovxlib=False)
        self.insert_version_number(self.testFile, version=self.version)


def main():
    ab = ApplicationBuilder(VERSION)
    ab.run()


if __name__ == '__main__':
    main()
