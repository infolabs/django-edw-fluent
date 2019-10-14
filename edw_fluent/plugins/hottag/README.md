1. в шаблоне подключения /alder/alder/plugins/block/templates/alder/plugins/block.html
и в CKEDITOR_CONFIGS добавлено:
'extraPlugins': 'hottag',
'allowedContent': true,
'extraAllowedContent': '*[*]{*}(*)'
и кнопка 'Hottag' в панель - ['Link', 'Unlink', 'Anchor', 'Hottag'],

В BlockPlugin добавлено
from edw_fluent.plugins.hottag.utils import update_hot_tags_on_render

def get_context(self, request, instance, **kwargs):
        # hottags
        if update_hot_tags_on_render:
            instance = update_hot_tags_on_render(instance)


2. Installed_apps
'edw_fluent.plugins.hottag',

FLUENT_TEXT_CLEAN_HTML = True

FLUENT_TEXT_PRE_FILTERS = (
   'edw_fluent.plugins.hottag.filters.hottag_filter',
)


3. urls.py
url(r'^hottagplugin/', include('edw_fluent.plugins.hottag.urls')),

4. миграции и collectstatic

5. Добавлена команда и таск update_hot_tags - обновляет ссылки
может принимать аргумент delta_days - количество дней ранее которых надо обновить ссылки
