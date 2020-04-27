from django import template
from django.utils.safestring import mark_safe
from django.conf.urls.static import static

from favicon.models import Favicon, config

register = template.Library()


@register.simple_tag(takes_context=True)
def place_favicon(context):
    """
    Gets Favicon-URL for the Model.

    Template Syntax:

        {% placeFavicon %}

    """
    fav = Favicon.objects.filter(isFavicon=True).first()
    if not fav:
        return mark_safe('<!-- no favicon -->')
    html = ''
    for rel in config:
        for size in sorted(config[rel], reverse=True):
            n = fav.get_favicon(size=size, rel=rel)
            html += f'<link rel="{n.rel}" sizes="{n.size}x{n.size}" href="{static(n.faviconImage.url)}"/>'

    default_fav = fav.get_favicon(size=32, rel='shortcut icon')
    html += f'<link rel="{default_fav.rel}" sizes="{default_fav.size}x{default_fav.size}"\
     href="{static(default_fav.faviconImage.url)}"/>'

    return mark_safe(html)
