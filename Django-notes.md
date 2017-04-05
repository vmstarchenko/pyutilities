- Views:
  * `django.http.HttpResponse`:
    Создает response объект.
    Пример:
    ```python
    def index():
        return HttpResponse(template.render(context)) # or just
        return HttpResponse("<html>...</html>")
    ```
  * `django.template.Context`

  * `django.template.loader.get_template`

  * `django.views.generic.base.TemplateView`:
    Можно переопределить аттрибут `template_name` и метод `get_context_data`.
    ```python
    class Foo(TemplateView):
        template_name = 'foo.html'

        def get_context_data(self, **kwargs):
            ctx = super(Foo, self).get_context_data(**kwargs)
            ... # do smth else with context
            return ctx
    ```

  * `django.shortcuts.render`
    ```python
    template = get_template(template_name)
    html = template.render(context)
    return HttpResponse(html)
    ```
    или
    ```python
    return render(request, template_name, context)
    ```

  * `django.shortcuts.render_to_response`
    То же что и `render` но не требует передачи `request`

- Urls
  * `django.conf.urls.url`
  * `django.conf.urls.include`


- Templates:
  * `static`: позволяет из django динамически передавать url путь к статике.
    Для этого в settings.py необходимо указать `STATIC_URL`.
    Требуется подключить как `{% load static %}`
    ```
    {% static 'app/style.css' %}
    ```

  * `extends`: отнаследоваться от шаблона
    ```
    {% extends 'base.html' %}
    ```

  * `block`: объявляет блок
    ```
    {% block content %}
    ...
    {% endblock %}
    ```

  * `csrf_token`
    ```
    {% csrf_token %}
    ```