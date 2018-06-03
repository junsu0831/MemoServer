from django.shortcuts import render
from .models import Memo

# Create your views here.
def memo_list(request):
    qs = Memo.objects.all()
    return render(request, 'memo/memo_list.html', {'memos': qs})

