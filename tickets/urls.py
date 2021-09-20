from django.urls import path
from django.views.generic import RedirectView

from .views import change_oil
from .views import diagnostic
from .views import inflate_tires
from .views import MenuView
from .views import ProcessingView
from .views import next_ticket
from .views import WelcomeView

app_name = "tickets"
urlpatterns = [
    path("", RedirectView.as_view(url="/menu")),
    path("welcome/", WelcomeView.as_view(), name="index"),
    path("menu/", MenuView.as_view(), name="menu"),
    path("get_ticket/change_oil", change_oil, name="change_oil"),
    path("get_ticket/inflate_tires", inflate_tires, name="inflate_tires"),
    path("get_ticket/diagnostic", diagnostic, name="diagnostic"),
    path("processing", ProcessingView.as_view(), name="processing"),
    path("processing/", RedirectView.as_view(url="/processing")),
    path("next", next_ticket, name="next_ticket"),
]
