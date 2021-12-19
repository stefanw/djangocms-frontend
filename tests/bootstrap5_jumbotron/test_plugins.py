from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.jumbotron.cms_plugins import (
    Bootstrap5JumbotronPlugin,
)

from ..fixtures import B5TestFixture


class B5JumbotronPluginTestCase(B5TestFixture, CMSTestCase):

    def test_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=Bootstrap5JumbotronPlugin.__name__,
            language=self.language,
        )
        plugin.full_clean()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="jumbotron">')

        # fluid option
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=Bootstrap5JumbotronPlugin.__name__,
            language=self.language,
            fluid=True,
        )
        plugin.full_clean()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="jumbotron jumbotron-fluid">')
