from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings

from ...cms_plugins import CMSUIPlugin
from .. import grid
from . import forms, models

mixin_factory = settings.get_renderer(grid)


@plugin_pool.register_plugin
class GridContainerPlugin(mixin_factory("GridContainer"), CMSUIPlugin):
    """
    Layout > Grid: "Container" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Container")
    module = _("Frontend")
    model = models.GridContainer
    form = forms.GridContainerForm
    change_form_template = "djangocms_frontend/admin/grid_container.html"
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
class GridRowPlugin(mixin_factory("GridRow"), CMSUIPlugin):
    """
    Layout > Grid: "Row" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Row")
    module = _("Frontend")
    model = models.GridRow
    form = forms.GridRowForm
    change_form_template = "djangocms_frontend/admin/grid_row.html"
    allow_children = True
    child_classes = ["GridColumnPlugin", "CardPlugin"]

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
            _("Responsive settings"),
            {
                "fields": ([f"row_cols_{size}" for size in settings.DEVICE_SIZES],),
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
        for x in range(data["create"] if data["create"] is not None else 0):
            extra = dict(column_alignment=None)
            for size in settings.DEVICE_SIZES:
                extra[f"{size}_col"] = data.get(f"create_{size}_col")
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


@plugin_pool.register_plugin
class GridColumnPlugin(mixin_factory("GridColumn"), CMSUIPlugin):
    """
    Layout > Grid: "Column" Plugin
    https://getbootstrap.com/docs/5.0/layout/grid/
    """

    name = _("Column")
    module = _("Frontend")
    model = models.GridColumn
    form = forms.GridColumnForm
    change_form_template = "djangocms_frontend/admin/grid_column.html"
    allow_children = True
    require_parent = True
    # TODO it should allow for the responsive utilitiy class
    # https://getbootstrap.com/docs/5.0/layout/grid/#column-resets
    parent_classes = ["GridRowPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    (
                        "column_alignment",
                        "text_alignment",
                    ),
                )
            },
        ),
        (
            _("Responsive settings"),
            {
                "fields": (
                    [f"{size}_col" for size in settings.DEVICE_SIZES],
                    [f"{size}_order" for size in settings.DEVICE_SIZES],
                    [f"{size}_offset" for size in settings.DEVICE_SIZES],
                    [f"{size}_ms" for size in settings.DEVICE_SIZES],
                    [f"{size}_me" for size in settings.DEVICE_SIZES],
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
