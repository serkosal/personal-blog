from django.forms import widgets


class PostContentWidget(widgets.Textarea):
    template_name = 'blog/editor_widget.html'

    def __init__(self, attrs=None):
        default_attrs = {'rows': '10', 'id': 'editorjs'}

        if attrs:
            default_attrs.update(attrs)

        super().__init__(default_attrs)
