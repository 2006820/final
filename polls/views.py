from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.views import generic

# Create your views here.
def write(request):
    return render(request, "polls/write.html")

# write에 받은거 DB 연동
def insert(request):
    # 데이터 베이스에 입력 처리 (idx 는 Oracle의 순번과 동일)
    addq = Question(question=request.POST['question'],
                  ans1=request.POST['ans1'],
                  ans2=request.POST['ans2'],
                  ans3=request.POST['ans3'],
                  ans4=request.POST['ans4'],
                  status=request.POST['status'],
                  )
    addq.save()
    return redirect("/polls/index")

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def delete(request):
    idv = request.POST['survey_idx']
    print("survey_idx:", idv)
    # delete * from address_address where idx = idv
    # 선택한 데이터의 레코드가 삭제됨
    addq = Question.objects.delete()
    return redirect('/polls/list')

# =====================================================
# 수정 기능
def update(request):
    idv = request.POST['survey_idx']
    question = request.POST['question']
    ans1 = request.POST['ans1']
    ans2 = request.POST['ans2']
    ans3 = request.POST['ans3']
    ans4 = request.POST['ans4']
    status = request.POST['status']

    print("survey_idx:", idv)
    print("question:", question)
    print("ans1:", ans1)
    print("ans2:", ans2)
    print("ans3:", ans3)
    print("ans4:", ans4)
    print("status:", status)

    # 수정 데이터 베이스 처리(idx=id -> 값을 넣으면 수정, 없으면 auto로 생성되므로 없어도됨)
    addq = Question(question=question, ans1=ans1, ans2=ans2, ans3=ans3, ans4=ans4, status=status)

    # 데이터 레코드가 수정됨
    addq.save()

    return redirect('/survey/list')

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     # return HttpResponse("You're looking at question %s." % question_id)
#     # try:
#     #    question = Question.objects.get(pk=question_id)
#     #except Question.DoesNotExist:
#     #    raise Http404("Question does not exist")
#     #return render(request, 'polls/detail.html', {'question': question})
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     #response = HttpResponse("You're looking at the results of question %s." % question_id)
#     #return response
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try: selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))