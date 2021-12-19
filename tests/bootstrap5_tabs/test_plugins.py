from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.tabs.cms_plugins import (
    Bootstrap5TabItemPlugin, Bootstrap5TabPlugin,
)

from ..fixtures import B5TestFixture


class B5TabsPluginTestCase(B5TestFixture, CMSTestCase):

    def test_tab_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=Bootstrap5TabPlugin.__name__,
            language=self.language,
        )
        plugin.full_clean()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'nav')
        self.assertContains(response, 'nav-tabs')

    def test_tab_item_plugin(self):
        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=Bootstrap5TabPlugin.__name__,
            language=self.language,
        )
        plugin = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=Bootstrap5TabItemPlugin.__name__,
            language=self.language,
            tab_title="tab title",
        )
        plugin.full_clean()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="tab-content">')
        self.assertContains(response, 'tab-pane')
