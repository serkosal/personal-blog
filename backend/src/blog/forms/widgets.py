"""File with post content html widget."""

from django.forms import widgets


class PostContentWidget(widgets.Textarea):
    """Post content html django widget."""
    
    template_name = 'blog/editor_widget.html'

    def __init__(self, attrs=None):
        """Construct PostContentWidget.
        
        Args:
            self: instance PostContentWidget.
            attrs: html attributes.
        
        """
        default_attrs = {'rows': '10', 'id': 'editorjs'}

        if attrs:
            default_attrs.update(attrs)

        super().__init__(default_attrs)
