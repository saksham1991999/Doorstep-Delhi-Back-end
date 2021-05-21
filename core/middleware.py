from core.models import ClientLog


class LogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def client_log(self, path, host, request_method, user_agent):
        ClientLog.objects.create(
            path=path,
            host=host,
            request_method=request_method,
            user_agent=user_agent
        )

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        if 'admin' not in request.path:
            self.client_log(
                request.path,
                request.headers['Host'],
                request.META['REQUEST_METHOD'],
                request.META['HTTP_USER_AGENT']
            )
        return response