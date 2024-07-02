from django import template
import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def split(string, sep):
   return string.split(sep)


register.filter("split", split)