from django.contrib.auth.models import User
from django.test import TestCase
from comment.models import Comment
from books.models import Book


"""
class to test model Comment
"""


class CommentTestCase(TestCase):


    def setUp(self):
        """
        Defined function before condition for test
        """

        user = User.objects.create(username='test', password='test')

        book = Book.objects.create(
            name="Harry Potter",
            description="is very good book",
            price=73.54
        )
        Comment.objects.create(
            book=book,
            name="Carlos",
            email="carlos@test.com",
            body="I like this post"
        )

        Comment.objects.create(
            book=book,
            name="Test",
            email="test@test.com",
            body="I like this post"
        )

    def test_comment_return_str(self):
        """
        Test string for comment
        """
        comment = Comment.objects.get(name="Carlos")
        self.assertEquals(comment.__str__(), "Comment I like this post by Carlos")

    def test_confirm_data(self):
        """
        Test confirm objects atributes
        """
        comment = Comment.objects.get(name="Carlos")
        self.assertEquals(comment.name, "Carlos")
        self.assertEquals(comment.email, "carlos@test.com")
        self.assertEquals(comment.body, "I like this post")

    def test_comment_orderind(self):
        """
        Test ordering comment
        """
        comments = Comment.objects.all()
        self.assertEquals(comments[0].name, "Test")
        self.assertEquals(comments[1].name, "Carlos")
        self.assertGreater(comments[0].created_on, comments[1].created_on)