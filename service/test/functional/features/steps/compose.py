#
# Copyright (c) 2014 ThoughtWorks, Inc.
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
from time import sleep

from behave import when
from common import *


@when('I compose a message with')
def impl(context):
    take_screenshot(context, '/tmp/screenshot.jpeg')
    toggle = context.browser.find_element_by_id('compose-mails-trigger')
    toggle.click()

    for row in context.table:
        fill_by_xpath(context, '//*[@id="subject"]', row['subject'])
        fill_by_xpath(context, '//*[@id="text-box"]', row['body'])


@when("for the '{recipients_field}' field I enter '{to_type}'")
def enter_address_impl(context, recipients_field, to_type):
    _enter_recipient(context, recipients_field, to_type + "\n")


@when("for the '{recipients_field}' field I type '{to_type}' and chose the first contact that shows")
def choose_impl(context, recipients_field, to_type):
    _enter_recipient(context, recipients_field, to_type)
    sleep(1)
    find_element_by_css_selector(context, '.tt-dropdown-menu div div').click()


@when('I save the draft')
def save_impl(context):
    context.browser.find_element_by_id('draft-button').click()


@when('I send it')
def send_impl(context):
    assert page_has_css(context, '#send-button[disabled]') is False
    context.browser.find_element(By.ID, 'send-button').click()
    # wait_until_element_is_deleted(context, (By.ID, 'send-button'), timeout=120)


def _enter_recipient(context, recipients_field, to_type):
    recipients_field = recipients_field.lower()
    browser = context.browser
    field = browser.find_element_by_css_selector('#recipients-%s-area .tt-input' % recipients_field)
    field.send_keys(to_type)
