from django.http import JsonResponse
from django.views import View


class BaseView(View):
    """Базовый класс, обрабатывающий исключения"""

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self._response({'errorMessage': e}, status=400
                                  )
        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params={'ensure_ascii': False},
        )
