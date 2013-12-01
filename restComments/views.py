import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from models import Comment
from forms import CommentForm
from serializers import CommentSerializer

logger = logging.getLogger('django.dev')

@api_view(['GET', 'POST'])
def comment_list(request, format=None):
    """
    List all comments, or create a new comment.
    """
    if request.method == 'GET':
        comments = Comment.objects.all()
        if format is None:
            form = CommentForm()
            data = {'form':form,'comments':comments}
            return Response(data, template_name='comments.html')
        else:
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        comment = Comment(userid=3)
        serializer = CommentSerializer(comment,request.DATA)
        logger.debug('point 2: ' + str(serializer.data))
        if serializer.is_valid():
            serializer.save()
            logger.debug('It is valid')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a comment instance.
    """
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''