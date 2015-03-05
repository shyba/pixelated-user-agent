#
# Copyright (c) 2015 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
from page import Page


class Sidebar(Page):
    '''
    Class to interact with sidebar. All interactions and validations of sidebar
    should be here.
    '''
    def __init__(self, webdriver):
        super(webdriver)

    def goto(self, where):
        tag = self.find_element_by_id('tag-%s' % where)
        tag.click()


    def gotoInbox(self):
        self.goto('inbox')

    def gotoDrafts(self):
        self.goto('drafts')

    def gotoSent(self):
        self.goto('sent')

    def gotoTrash(self):
        self.goto('trash')

    def gotoAll(self):
        self.goto('all')

    def open_sidebar(self):

    def close_sidebar(self):

    def selectEmailsWithTag(self, tag):
        self.open_sidebar()


