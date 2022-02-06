from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.http import HttpRequest

from djangocms_frontend.contrib.image.cms_plugins import ImagePlugin
from djangocms_frontend.contrib.image.forms import ImageForm, get_templates

from ..fixtures import TestFixture
from ..helpers import get_filer_image


class PicturePluginTestCase(TestFixture, CMSTestCase):
    def setUp(self):
        super().setUp()
        self.image = get_filer_image()

    def tearDown(self):
        super().tearDown()
        self.image.delete()

    def test_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=ImagePlugin.__name__,
            language=self.language,
            config={
                "picture": {"pk": self.image.id, "model": "filer.Image"},
                "use_responsive_image": "yes",
            },
        )
        plugin.initialize_from_form(ImageForm)
        plugin.save()
        self.assertTrue(plugin.is_responsive_image)

        self.page.publish(self.language)
        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="img-fluid"')

        # test picture_fluid, picture_rounded and picture_thumbnail options
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=ImagePlugin.__name__,
            language=self.language,
            config={
                "image": {"pk": self.image.id, "model": "filer.Image"},
                "picture_fluid": False,
                "picture_rounded": True,
                "picture_thumbnail": True,
            },
        )
        plugin.initialize_from_form(ImageForm)
        plugin.save()
        self.page.publish(self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ('class="img-thumbnail rounded"' in response.content.decode("utf-8"))
            or ('class="rounded img-thumbnail"' in response.content.decode("utf-8")),
            f'class="img-thumbnail rounded" not found in {response.content.decode("utf-8")}',
        )

    def test_image_form(self):
        request = HttpRequest()
        request.POST = {
            "template": get_templates()[0][0],
            "picture": "",
            "external_picture": "https://www.django-cms.com/",
            "use_responsive_image": "yes",
        }
        form = ImageForm(request.POST)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["config"]["use_responsive_image"], "yes")

        request.POST.update(
            {
                "use_automatic_scaling": True,
                "use_no_cropping": True,
            }
        )
        form = ImageForm(request.POST)
        self.assertFalse(form.is_valid())
        self.assertFalse(form.is_valid())