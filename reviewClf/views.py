from django.shortcuts import render, HttpResponse
from .forms import ReviewForm
from .classifiers import get_prediction

# Create your views here.


def enter_review(request):
    message = ""
    words = []
    if request.method != 'POST':
        # Supply blank form
        form = ReviewForm()
    else:
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            if len(form.data['text'].split()) == 0:
                message = "Your review was too short to process."
                form = ReviewForm()
            else:
                label, prob, words = get_prediction(form.data['text'])
                prob = str(round(prob * 100, 2))
                return render(request, 'reviewClf/show_prediction.html', {'result': label.title(),
                                                                          'prob': prob,
                                                                          'words': words})
    context = {'form': form, 'message': message, 'words': words}
    return render(request, 'reviewClf/enter_review.html', context)
