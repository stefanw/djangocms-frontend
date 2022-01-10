from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.helpers import concat_classes

from . import forms, models
from .constants import GRID_COLUMN_CHOICES


@plugin_pool.register_plugin
class GridContainerPlugin(CMSPluginBase):
    """
    Layout > Grid: "Container" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Container")
    module = _("Interface")
    model = models.GridContainer
    form = forms.GridContainerForm
    render_template = f"djangocms_frontend/{settings.framework}/grid_container.html"
    allow_children = True

    fieldsets = [
        (None, {"fields": ("container_type",)}),
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


@plugin_pool.register_plugin
class GridRowPlugin(CMSPluginBase):
    """
    Layout > Grid: "Row" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Row")
    module = _("Interface")
    model = models.GridRow
    form = forms.GridRowForm
    change_form_template = "djangocms_frontend/admin/grid_row.html"
    render_template = f"djangocms_frontend/{settings.framework}/grid_row.html"
    allow_children = True
    child_classes = ["GridColumnPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "create",
                    ("vertical_alignment", "horizontal_alignment"),
                )
            },
        ),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    (
                        "tag_type",
                        "gutters",
                    ),
                    "attributes",
                ),
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        data = form.cleaned_data
        for x in range(
            data["config"]["create"] if data["config"]["create"] is not None else 0
        ):
            extra = dict(column_type=GRID_COLUMN_CHOICES[0][0], column_alignment=None)
            for size in settings.DEVICE_SIZES:
                extra[f"{size}_col"] = data.get("create_{}_col".format(size))
                extra[f"{size}_order"] = None
                extra[f"{size}_offset"] = None
                extra[f"{size}_ml"] = None
                extra[f"{size}_mr"] = None
            col = models.GridColumn(
                parent=obj,
                placeholder=obj.placeholder,
                language=obj.language,
                position=obj.numchild,
                plugin_type=GridColumnPlugin.__name__,
                ui_item=models.GridColumn.__class__.__name__,
                config=extra,
            )
            obj.add_child(instance=col)

    def render(self, context, instance, placeholder):
        gutter = "no-gutters" if instance.gutters else ""  # CHECK
        classes = concat_classes(
            [
                "row",
                instance.vertical_alignment,
                instance.horizontal_alignment,
                gutter,
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = classes

        return super().render(context, instance, placeholder)


@plugin_pool.register_plugin
class GridColumnPlugin(CMSPluginBase):
    """
    Layout > Grid: "Column" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Column")
    module = _("Interface")
    model = models.GridColumn
    form = forms.GridColumnForm
    change_form_template = "djangocms_frontend/admin/grid_column.html"
    render_template = f"djangocms_frontend/{settings.framework}/grid_column.html"
    allow_children = True
    require_parent = True
    # TODO it should allow for the responsive utilitiy class
    # https://getbootstrap.com/docs/5.0/layout/grid/#column-resets
    parent_classes = ["GridRowPlugin"]

    fieldsets = [
        (None, {"fields": (("column_type", "column_alignment"),)}),
        (
            _("Responsive settings"),
            {
                "fields": (
                    ["{}_col".format(size) for size in settings.DEVICE_SIZES],
                    ["{}_order".format(size) for size in settings.DEVICE_SIZES],
                    ["{}_offset".format(size) for size in settings.DEVICE_SIZES],
                    ["{}_ml".format(size) for size in settings.DEVICE_SIZES],
                    ["{}_mr".format(size) for size in settings.DEVICE_SIZES],
                )
            },
        ),
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
        column = ""
        classes = instance.get_grid_values()

        if classes:
            column += "{}".format(" ".join(cls for cls in classes if cls))

        attr_classes = concat_classes(
            [
                instance.column_type,
                column,
                instance.column_alignment,
                instance.attributes.get("class"),
            ]
        )
        instance.attributes["class"] = attr_classes

        return super().render(context, instance, placeholder)