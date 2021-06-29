from django.urls import path
from . import views


urlpatterns = [
    path('chip_tuning', views.chip_tuning, name="chip_tuning"),
    path('engine_rebuilds', views.engine_rebuilds, name="engine_rebuilds"),
    path('servicing_and_repairs', views.servicing_and_repairs,
         name="servicing_and_repairs"),
    path('diagnostics', views.diagnostics, name="diagnostics"),
    path('custom_exhausts', views.custom_exhausts, name="custom_exhausts"),
    path('wheel_repair', views.wheel_repair, name="wheel_repair"),
    path('corner_weight_setup', views.corner_weight_setup,
         name="corner_weight_setup"),
    path('track_drift_preparation', views.track_drift_preparation,
         name="track_drift_preparation"),
]
