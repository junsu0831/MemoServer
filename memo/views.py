# pylint: disable=E1101
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Memo
from .forms import MemoForm

from .serializers import MemoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from datetime import date, timedelta
from operator import itemgetter
import re
import operator

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
def memo_time(request):
    qs = Memo.objects.exclude(related_date__isnull=True).filter(related_date__gte=date.today()).order_by("related_date")[:10]
    return render(request, 'memo/memo_list.html', {'memos' : qs})


def memo_top10(request):
    qs = Memo.objects.all().order_by("-created_date")[:10]
    qs_list = list(qs)
    memo_list = []
    result_list = []

    score = 10
    for memo in qs_list:
        dic = {"memo" : memo}
        dic["score"] = score
        memo_list.append(dic)
        score = score - 1
    
    qs = Memo.objects.exclude(related_date__isnull=True).filter(related_date__gte=date.today()).order_by("related_date")[:10]
    qs_list = list(qs)

    score = 10
    for memo in qs_list:
        dic = {"memo" : memo}
        delta = memo.related_date - date.today()

        if delta <= timedelta(days=2):
            dic["score"] = 10
        elif delta <= timedelta(days=4):
            dic["score"] = 5
        elif delta <= timedelta(days=7):
            dic["score"] = 4
        else:
            dic["score"] = 0

        for r_dic in memo_list:
            if r_dic["memo"] == dic["memo"]:
                if r_dic["score"] < dic["score"]:
                    memo_list.remove(r_dic)
                    memo_list.append(dic)
    
    memo_list = sorted(memo_list, key=itemgetter('score'), reverse=True) 

    for dic in memo_list[0:10]:
        memo = dic["memo"]
        result_list.append(memo)

    return render(request, 'memo/memo_list.html', {'memos' : result_list})


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
            memo.related_date = get_related_date(memo.text)
            memo.save()
            return redirect('memo_list')
    else:
        form = MemoForm()
    return render(request, 'memo/memo_edit.html', {'form': form})

def get_related_date(text):
    # 00월 00일 문자 패턴
    p = re.compile(r"(?P<month>\d+)\s*월\s*(?P<day>\d+)\s*일")
    m = p.search(text)

    if m:
        month = m.group('month')
        day = m.group('day')
        related_date = date(date.today().year, int(month), int(day))
        return related_date

    # 내일 모레를 날짜로 변환
    p = re.compile(r"내일\s*모레")
    m = p.search(text)

    if m:
        related_date = date(date.today().year, date.today().month, date.today().day + 3)
        return related_date

    # 내일을 날짜로 변환
    p = re.compile(r"내일")
    m = p.search(text)

    if m:
        related_date = date(date.today().year, date.today().month, date.today().day + 1)
        return related_date

    return None
