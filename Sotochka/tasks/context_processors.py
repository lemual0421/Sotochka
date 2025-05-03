from django.conf import settings

def mathjax(request):
    """
    Добавляет переменную mathjax в контекст шаблонов,
    если в настройках включена поддержка MathJax
    """
    return {
        'mathjax': getattr(settings, 'MATHJAX_ENABLED', True)
    }