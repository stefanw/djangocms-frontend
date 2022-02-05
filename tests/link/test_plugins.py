from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_frontend.contrib.link.cms_plugins import LinkPlugin
from djangocms_frontend.contrib.link.forms import LinkForm, SmartLinkField

from ..fixtures import TestFixture


class LinkPluginTestCase(TestFixture, CMSTestCase):
    def test_plugin(self):
        add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
            ),
        ).initialize_from_form(LinkForm).save()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="https://www.divio.com"')

        # add more options
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
                link_context="primary",
                link_size="btn-sm",
                link_block=True,
                name="django CMS rocks!",
            ),
        )
        plugin.initialize_from_form(LinkForm).save()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "text-primary")
        self.assertContains(response, "btn-sm")
        self.assertContains(response, "btn-block")

        # alternate version for link_type
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                internal_link=dict(model="cms.page", pk=self.page.id),
                link_context="primary",
                link_type="btn",
                name="django CMS rocks!",
            ),
        )
        plugin.initialize_from_form(LinkForm).save()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "btn-primary")
        self.assertContains(response, 'href="/content/"')

        # alternate version broken link
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                internal_link=dict(model="cms.page", pk=-3141),
                link_context="primary",
                link_type="btn",
                link_outline=True,
                name="django CMS rocks!",
            ),
        )
        plugin.initialize_from_form(LinkForm).save()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\ndjango CMS rocks")

        # alternate version using link_outline
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=LinkPlugin.__name__,
            language=self.language,
            config=dict(
                external_link="https://www.divio.com",
                link_context="primary",
                link_type="btn",
                link_outline=True,
            ),
        )
        plugin.initialize_from_form(LinkForm).save()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ('class="btn btn-outline-primary"' in response.content.decode("utf-8"))
            or ('class="btn-outline-primary btn"' in response.content.decode("utf-8")),
            f'Cound not find class="btn btn-outline-primary" in {response.content.decode("utf-8")}',
        )

    def test_smart_link_field(self):
        slf = SmartLinkField()
        choices = slf.get_link_choices()
        self.assertIn(("", "----"), choices)
        self.assertEqual("example.com", choices[1][0])  # Site name
        self.assertIn(("2-1", "home"), choices[1][1])

        cleaned = slf.clean("2-1")
        self.assertEqual(dict(model="cms.page", pk=1), cleaned)

        self.assertEqual(slf.prepare_value("blabla"), "")
        self.assertEqual(slf.prepare_value(dict(model="cms.page", pk=1)), "2-1")
        self.assertEqual(slf.prepare_value(self.home), "2-1")
