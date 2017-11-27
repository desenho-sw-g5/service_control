from django import template
from modules.models import ModuleControl

register = template.Library()

@register.simple_tag
def call_action(action, *args, **kwargs):
    mc = ModuleControl()
    return mc.call_action(action, *args, **kwargs)