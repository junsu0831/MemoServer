# pylint: disable=E1101
from django.shortcuts import render, redirect
from .models import Memo
from .forms import MemoForm

# Create your views here.
def memo_list(request):
    qs = Memo.objects.all()

    q = request.GET.get('q', '')
    if q:
        result_qs = qs.filter(title__icontains=q)
        result_qs |= qs.filter(text__icontains=q)
        qs = result_qs

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
    return render(request, 'memo/memo_edit.html', {'form' : form})