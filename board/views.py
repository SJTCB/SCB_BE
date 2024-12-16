


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Board, Comment
from .serializers import (
    BoardSerializer,
    BoardListSerializer,
    BoardDetailSerializer,
    BoardUpdateSerializer,
    CommentSerializer
)

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']  # PUT 제거

    def get_serializer_class(self):
        """Serializer 반환"""
        if self.action == 'list':
            return BoardListSerializer  # 목록 조회
        elif self.action == 'retrieve':
            return BoardDetailSerializer  # 상세 조회
        elif self.action in ['update', 'partial_update']:
            return BoardUpdateSerializer  # 수정용 Serializer
        return BoardSerializer  # 기본 생성/수정 Serializer

    @action(detail=True, methods=['get'], url_path='comments')
    def list_comments(self, request, pk=None):
        """특정 게시물의 댓글 조회"""
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response({"error": "Board not found."}, status=status.HTTP_404_NOT_FOUND)

        comments = board.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='comments')
    def add_comment(self, request, pk=None):
        """특정 게시물에 댓글 추가"""
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response({"error": "Board not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(board=board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='comments/(?P<comment_id>[^/.]+)')
    def delete_comment(self, request, pk=None, comment_id=None):
        """특정 게시물의 댓글 삭제"""
        try:
            board = self.get_object()
            comment = board.comments.get(id=comment_id)
            comment.delete()
            return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']  # PUT 제거

    def create(self, request, *args, **kwargs):
        """댓글 생성"""
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """댓글 수정"""
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """댓글 삭제"""
        return super().destroy(request, *args, **kwargs)
