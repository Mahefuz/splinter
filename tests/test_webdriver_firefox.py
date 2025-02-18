# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest

import pytest

from .fake_webapp import EXAMPLE_APP
from .base import WebDriverTests, get_browser


class FirefoxBrowserTest(WebDriverTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = get_browser('firefox', fullscreen=False)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.visit(EXAMPLE_APP)


class FirefoxBrowserFullScreenTest(WebDriverTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = get_browser('firefox', fullscreen=True)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self):
        self.browser.visit(EXAMPLE_APP)


def test_firefox_create_instance_with_extension(request):
    """Test: Load an extension via selenium.

    The dummy extension should add a red border to any web page.
    """
    extension_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'dummy_extension',
        'borderify-1.0-an+fx.xpi',
    )

    browser = get_browser('firefox', extensions=[extension_path])
    request.addfinalizer(browser.quit)

    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_css('body')
    style = elem._element.get_attribute('style')
    assert "border: 5px solid red;" == style


def test_preference_set(request):
    preferences = {
        "dom.max_script_run_time": 360,
        "devtools.inspector.enabled": True,
    }
    browser = get_browser('firefox', profile_preferences=preferences)
    request.addfinalizer(browser.quit)

    preferences = browser.driver.profile.default_preferences
    assert "dom.max_script_run_time" in preferences

    value = preferences.get("dom.max_script_run_time")
    assert int(value) == 360


def test_capabilities_set(request):
    browser = get_browser('firefox', capabilities={"pageLoadStrategy": "eager"})
    request.addfinalizer(browser.quit)

    capabilities = browser.driver.capabilities
    assert "pageLoadStrategy" in capabilities
    assert "eager" == capabilities.get("pageLoadStrategy")
