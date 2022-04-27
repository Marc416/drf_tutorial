from django.contrib.auth.models import User

from rest_framework import generics, permissions

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer


# 유저나 snippet만으로 향하는 단일 api 가 없으므로 이렇게 만들어준다.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # 2가지가 지켜져야 한다.
        # 1. restframework의 reverse를 써야 한다.
        # 2. 추후에 작성될 url이름이 알아보기 쉬워야 한다.
        # 다른 엔드포인트들과 다르게 아래의 컨텍스트들은 json이아닌 html타입으로 전달할 것이다.
        # REST Framework 에는 2가지 방법이 있는데
        # 1. template을 이용하는 방법
        # 2. 미리 렌더된 html을 사용하는 것.
        # 두번째 방법을 이번에 사용할 것이다.
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # The create() method of our serializer will now be passed
    # an additional 'owner' field, along with the validated data
    # from the request.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# 명확한 ggeneric 뷰가 없으므로 베이스클래스를 이용합니다.
class SnippetHighlight(generics.GenericAPIView):
    """
    snippets 만을 보여주는 뷰
    """
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
