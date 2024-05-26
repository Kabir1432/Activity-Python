from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from activityngo.question_types.models import (DropdownQuestion,
                                               DropdownQuestionOption,
                                               EssayQuestion, ExitTestQuestion,
                                               ExitTestQuestionOption,
                                               McqOption, MCQQuestion,
                                               NumericQuestion,
                                               PercentageQuestion,
                                               ShortAnswerQuestion,
                                               TaskInstructions,
                                               UploadPhotoQuestion,
                                               VideoQuestion)
from activityngo.question_types.serializers import (
    DropdownQuestionOptionSerializer, DropdownQuestionSerializer,
    EssayQuestionSerializer, ExitTestQuestionOptionSerializer,
    ExitTestQuestionSerializer, MCQOptionSerializer, MCQQuestionSerializer,
    NumericQuestionSerializer, PercentageQuestionSerializer,
    ShortAnswerQuestionSerializer, TaskInstructionsSerializer,
    UploadPhotoQuestionSerializer, VideoQuestionSerializer)
from activityngo.utils.permissions import IsAPIKEYAuthenticated


class VideoQuestionViewSet(viewsets.ModelViewSet):
    queryset = VideoQuestion.objects.all()
    serializer_class = VideoQuestionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]


class EssayQuestionViewSet(viewsets.ModelViewSet):
    queryset = EssayQuestion.objects.all()
    serializer_class = EssayQuestionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]


class ShortAnswerQuestionViewSet(viewsets.ModelViewSet):
    queryset = ShortAnswerQuestion.objects.all()
    serializer_class = ShortAnswerQuestionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]


class NumericQuestionViewSet(viewsets.ModelViewSet):
    queryset = NumericQuestion.objects.all()
    serializer_class = NumericQuestionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]


class PercentageQuestionViewSet(viewsets.ModelViewSet):
    queryset = PercentageQuestion.objects.all()
    serializer_class = PercentageQuestionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]


class MCQQuestionViewSet(viewsets.ModelViewSet):
    queryset = MCQQuestion.objects.all()
    serializer_class = MCQQuestionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]


class MCQOptionViewSet(viewsets.ModelViewSet):
    queryset = McqOption.objects.all()
    serializer_class = MCQOptionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["mcq_question__id"]


class UploadPhotoQuestionViewSet(viewsets.ModelViewSet):
    queryset = UploadPhotoQuestion.objects.all()
    serializer_class = UploadPhotoQuestionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]


class ExitTestQuestionViewSet(viewsets.ModelViewSet):
    queryset = ExitTestQuestion.objects.all()
    serializer_class = ExitTestQuestionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]


class ExitTestQuestionOptionViewSet(viewsets.ModelViewSet):
    queryset = ExitTestQuestionOption.objects.all()
    serializer_class = ExitTestQuestionOptionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["exit_test_question__id"]


class DropdownQuestionViewSet(viewsets.ModelViewSet):
    queryset = DropdownQuestion.objects.all()
    serializer_class = DropdownQuestionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]


class DropdownQuestionOptionViewSet(viewsets.ModelViewSet):
    queryset = DropdownQuestionOption.objects.all()
    serializer_class = DropdownQuestionOptionSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["dropdown_question__id"]


class TaskInstructionsViewSet(viewsets.ModelViewSet):
    queryset = TaskInstructions.objects.all()
    serializer_class = TaskInstructionsSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["project__id"]
