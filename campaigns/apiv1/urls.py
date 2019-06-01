from django.urls import path

from campaigns.apiv1.views import CampaignSubscriptionCreateAPIView, CampaignSubscriptionListAPIView

app_name = 'campaigns-api-v1'
urlpatterns = [
    path('subscribe/', CampaignSubscriptionCreateAPIView.as_view(), name='subscribe'),
    path('subscriptions/', CampaignSubscriptionListAPIView.as_view(), name='subscriptions'),
]
