from rest_framework.routers import DefaultRouter

from apps.doc.views import DocViewSet

router = DefaultRouter()
router.register("doc", DocViewSet)

urlpatterns = router.urls
