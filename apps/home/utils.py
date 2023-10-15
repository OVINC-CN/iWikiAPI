import datetime
import xml.dom.minidom

from django.conf import settings

from apps.doc.models import Doc


class Sitemap:
    """
    Generate Sitemap for SEO
    """

    SITEMAP_STATIC_URLS = [
        "/",
    ]

    def __init__(self):
        self.tree = xml.dom.minidom.Document()
        self.root = self.tree.createElement("urlset")
        self.add_root()
        self.add_static()
        self.add_imgs()

    def add_root(self) -> None:
        self.root.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        self.root.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        self.root.setAttribute(
            "xsi:schemaLocation",
            "http://www.sitemaps.org/schemas/sitemap/0.9 \
                    http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd",
        )
        self.tree.appendChild(self.root)

    def add_static(self) -> None:
        for url in self.SITEMAP_STATIC_URLS:
            self._add_path(url)

    def add_imgs(self) -> None:
        docs = Doc.objects.filter(is_public=True)
        for doc in docs:
            self._add_path(f"/doc/{doc.id}")

    def _add_path(self, path) -> None:
        node_url = self.tree.createElement("url")
        node_loc = self.tree.createElement("loc")
        node_loc.appendChild(self.tree.createTextNode(settings.FRONTEND_URL + str(path)))
        node_lastmod = self.tree.createElement("lastmod")
        node_lastmod.appendChild(self.tree.createTextNode(str(datetime.datetime.now().date())))
        node_url.appendChild(node_loc)
        node_url.appendChild(node_lastmod)
        self.root.appendChild(node_url)
