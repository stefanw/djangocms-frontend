from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import concat_classes

from ... import settings
from . import forms, models


@plugin_pool.register_plugin
class JumbotronPlugin(CMSPluginBase):
    """
    Components > "Jumbotron" Plugin
    https://getbootstrap.com/docs/5.0/components/jumbotron/
    """

    name = _("Jumbotron")
    module = _("Frontend")
    model = models.Jumbotron
    form = forms.JumbotronForm
    render_template = f"djangocms_frontend/{settings.framework}/jumbotron.html"
    change_form_template = "djangocms_frontend/admin/jumbotron.html"
    allow_children = True

    fieldsets = [
        (None, {"fields": ("jumbotron_fluid",)}),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]

    def render(self, context, instance, placeholder):
        link_classes = ["jumbotron"]
        if instance.jumbotron_fluid:
            link_classes.append("jumbotron-fluid")

        classes = concat_classes(
            link_classes
            + [
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)
