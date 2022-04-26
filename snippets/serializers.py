from django.contrib.auth.models import User, Group
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


# Serializer는 장고의 Form과 비슷하
# serializers.Serialzer 에 장고 model 이 들어 갈 수 있는 가본데 어떻게 되는지 모르겠다.
class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # Under equivalent to using widget=widgets.Textarea
    # This is particularly useful for controlling how the browsable API should be displayed
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    # Serializers with many=True do not support multiple update by default, only multiple create.
    # many=true 여야 다중속성을 시리얼라이즈화 할 수 있다.
    # snippets 는 user 모델의 역관계라서 명시적으로 필드를 추가해줘야 한다.
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    # Auth 인증 유저만
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        # Serializer에 새로운 필드가 추가되면 Meta 클래스의 fields에 추가해줘야한다.
        fields = ['id', 'username', 'snippets', 'owner']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
