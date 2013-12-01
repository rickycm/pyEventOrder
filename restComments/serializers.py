__author__ = 'Aston'

from rest_framework import serializers
from models import Comment

class CommentSerializer(serializers.Serializer):
    userid = serializers.IntegerField(required=False)
    post = serializers.CharField(required=True)
    answer = serializers.CharField(required=False)
    created = serializers.DateTimeField(required=False)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.userid = attrs.get('userid', instance.userid)
            instance.post = attrs.get('post', instance.post)
            instance.answer = attrs.get('answer', instance.answer)
            instance.created = attrs.get('created', instance.created)
            return instance
        return Comment(**attrs)