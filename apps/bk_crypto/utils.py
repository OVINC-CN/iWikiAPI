from typing import Union

from bkcrypto.contrib.django.fields import SymmetricTextField
from django.conf import settings

from apps.doc.models import Comment, CommentBin, Doc, DocBin


class DataEncryptHelper:
    """
    Help Encrypt or Decrypt All Data
    """

    def __init__(self):
        self.field = SymmetricTextField()
        if settings.ENABLE_BKCRYPTO:
            # when save to db, orm will auto encrypt data
            self.method: callable = lambda content: content
        else:
            # needs decrypt
            self.method = self.field.get_decrypted_value

    def trans(self) -> None:
        [self.trans_doc(d) for d in [*Doc.objects.all(), *DocBin.objects.all()]]  # pylint: disable=W0106
        [self.trans_comment(c) for c in [*Comment.objects.all(), *CommentBin.objects.all()]]  # pylint: disable=W0106

    def trans_doc(self, doc: Union[Doc, DocBin]) -> None:
        doc.title = self.method(doc.title)
        doc.content = self.method(doc.content)
        doc.header_img = self.method(doc.header_img)
        doc.save(update_fields=["title", "content", "header_img"])

    def trans_comment(self, comment: Union[Comment, CommentBin]) -> None:
        comment.content = self.method(comment.content)
        comment.save(update_fields=["content"])
