from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    # validating image properties using rest framework's field level
    # validation method
    # using this naming convetion, this method will be called automatically
    # and valudate teh uploaded image every time we create or update a post
    def validate_image(self, value):
        # checking if file size is bigger than 2mb limit
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size greater than 2MB'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width greater than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height greater than 4096px'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image',
            'image_filter'
        ]