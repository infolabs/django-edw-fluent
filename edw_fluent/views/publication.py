# -*- coding: utf-8 -*-

from django.db.models import F
from django.shortcuts import redirect

from edw.views.entity import EntityViewSet

from edw_fluent.models.publication import PublicationBase


# =========================================================================================================
# PublicationViewSet
# =========================================================================================================
class PublicationViewSet(EntityViewSet):
    """
    RUS: Класс для отображения публикаций.
    """
    def retrieve(self, request, *args, **kwargs):
        """
        RUS: Извлекает публикации после применения сериалайзера.
        """
        return super(PublicationViewSet, self).retrieve(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        """
        RUS: Вспомогательная функция после отработки сериалайзера устанавливает cookie,
        перенаправляет на сайт по указанному адресу.
        """
        if self.action == 'retrieve':
            pk = response.data.get('id', None)
            if pk is not None:
                cookie_name = "_seen_{}".format(pk)
                if cookie_name not in request.COOKIES:
                    response.set_cookie(cookie_name, '1')
                    PublicationBase.objects.filter(id=pk).update(statistic=F('statistic') + 1)

            for characteristic in response.data.get('characteristics', []):
                if characteristic['path'] == 'entity/publication_wrapper/redirect-url':
                    try:
                        link = characteristic['values'][0]
                    except IndexError:
                        pass
                    else:
                        return redirect(link, permanent=True)

        return super(EntityViewSet, self).finalize_response(request, response, *args, **kwargs)
