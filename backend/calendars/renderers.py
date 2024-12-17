from rest_framework import renderers

class ICSRenderer(renderers.BaseRenderer):
    media_type = 'text/calendar'
    format = 'ics'
    charset = 'utf-8'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data