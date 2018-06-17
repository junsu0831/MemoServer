# pylint: disable=E1101
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Memo
from .forms import MemoForm
import json

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
            message = "메모가 하나도 없다."
            return render(request, 'memo/memo_list.html', {'msg' : message})

    return render(request, 'memo/memo_list.html', {'memos' : qs})


def memo_list_json(request):
    memos_dic = {}
    records_list = []
    qs = Memo.objects.all().order_by('-created_date')

    for memo in qs:
        title = memo.title
        text = memo.text
        record = {"title":title, "text":text}
        records_list.append(record)
    
    memos_dic["memos"] = records_list
    return HttpResponse(json.dumps(memos_dic, ensure_ascii=False), content_type="application/json")



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
