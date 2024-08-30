from django.shortcuts import render

def word_directory_view(request):
    return render(request, 'mypage/word-diretory.html')