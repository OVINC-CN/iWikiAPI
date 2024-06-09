from channels.db import database_sync_to_async
from django.conf import settings
from django.conf.global_settings import LANGUAGE_COOKIE_NAME
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from ovinc_client.account.models import User
from ovinc_client.account.serializers import UserInfoSerializer
from ovinc_client.core.auth import SessionAuthenticate
from ovinc_client.core.viewsets import ListMixin, MainViewSet
from rest_framework.response import Response

from apps.home.serializers import I18nRequestSerializer
from apps.home.utils import Sitemap

USER_MODEL: User = get_user_model()


class HomeView(MainViewSet):
    """
    Home View
    """

    queryset = USER_MODEL.get_queryset()
    authentication_classes = [SessionAuthenticate]

    async def list(self, request, *args, **kwargs):
        msg = f"[{request.method}] Connect Success"
        return Response({"resp": msg, "user": await UserInfoSerializer(instance=request.user).adata})


class SitemapView(ListMixin, MainViewSet):
    """
    Sitemap View
    """

    authentication_classes = [SessionAuthenticate]

    async def list(self, request, *args, **kwargs):
        sitemap = await database_sync_to_async(Sitemap)()
        return HttpResponse(content=sitemap.tree.toxml(), content_type="application/xml")


class I18nViewSet(MainViewSet):
    """
    International
    """

    authentication_classes = [SessionAuthenticate]

    async def create(self, request, *args, **kwargs):
        """
        Change Language
        """

        # Varify Request Data
        request_serializer = I18nRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_data = request_serializer.validated_data

        # Change Lang
        lang_code = request_data["language"]
        response = Response()
        response.set_cookie(
            LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.SESSION_COOKIE_AGE,
            domain=settings.SESSION_COOKIE_DOMAIN,
        )
        return response


class FeatureView(ListMixin, MainViewSet):
    """
    Feature Toggle
    """

    authentication_classes = [SessionAuthenticate]

    async def list(self, request, *args, **kwargs):
        """
        List all features
        """

        return Response(
            data={
                # Encrypt disabled and search type configured
                "doc_fuzzy_search": (not settings.ENABLE_BKCRYPTO and bool(settings.DOC_SEARCH_TYPE))
            }
        )
