# pylint: disable=E1101
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Memo
from .forms import MemoForm

from .serializers import MemoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def memo_rest(request, format=None):
    if request.method == 'GET':
        qs = Memo.objects.all().order_by("-created_date")
        serializer = MemoSerializer(qs, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
def memo_list(request):
    qs = Memo.objects.all().order_by("-created_date")

    q = request.GET.get('q', '')
    if q:
        result_qs = qs.filter(title__icontains=q)
        result_qs |= qs.filter(text__icontains=q)
        if not result_qs:
            message = "검색 결과가 없습니다."
            return render(request, 'memo/memo_list.html', {'msg' : message})
        qs = result_qs
    else:
        if not qs:
            message = "저장된 메모가 없습니다. 새로운 메모를 추가하세요."
            return render(request, 'memo/memo_list.html', {'msg' : message})

    return render(request, 'memo/memo_list.html', {'memos' : qs})


def memo_new(request):
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = Memo()
            memo.title = form.cleaned_data['title']
            memo.text = form.cleaned_data['text']
            memo.author = request.user
            memo.save()
            return redirect('memo_list')
    else:
        form = MemoForm()
    return render(request, 'memo/memo_edit.html', {'form': form})
