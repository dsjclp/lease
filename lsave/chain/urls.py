from django.conf.urls import url, include

app_name = 'chain'

urlpatterns = [
    url(r'^api/v0/', include('chain.api.v0.urls'), name='api'),
]
