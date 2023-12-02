from rest_framework.routers import DefaultRouter

from apps.home.views import FeatureView, HomeView, I18nViewSet, SitemapView

router = DefaultRouter()
router.register("", HomeView)
router.register("sitemap", SitemapView, basename="sitemap")
router.register("i18n", I18nViewSet, basename="i18n")
router.register("features", FeatureView, basename="feature")

urlpatterns = router.urls
