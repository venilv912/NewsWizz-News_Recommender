# in recommender/views.py
from django.shortcuts import render, get_object_or_404, redirect
import random
from . import models
from . import mlmodel  # Import your recommendation function

def random_article(request):
    # Get a random article
    random_recommendations = random.sample(list(models.Article.objects.all()), 10)
    context = {'recommendations': random_recommendations}
    return render(request, 'random_article.html', context)


def article_link_and_recommendations(request, article_id):
    # Get the selected article
    article = get_object_or_404(models.Article, pk=article_id)

    new_article_id = request.GET.get('new_article_id')
    if new_article_id:
        new_article=get_object_or_404(models.Article,pk=new_article_id)
        result=mlmodel.tfidf_based_model(new_article.rowid,11)
        recommendation_ids=[row[0] for row in result ]
        recommendations=models.Article.objects.filter(rowid__in=recommendation_ids)

    else:
        result=mlmodel.tfidf_based_model(article.rowid,11)
        recommendation_ids=[row[0] for row in result ]
        recommendations=models.Article.objects.filter(rowid__in=recommendation_ids)

    return render(request, 'recommendations.html', {'article': article, 'recommendations': recommendations})

def redirect_to_article(request, article_id):
    article = get_object_or_404(models.Article, pk=article_id)
    return redirect(article.article_link)
