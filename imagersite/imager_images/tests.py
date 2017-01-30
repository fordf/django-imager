from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from imager_images.models import Photo, Album
from imager_profile.tests import UserFactory
import factory
from django.urls import reverse_lazy
from faker import Faker
from bs4 import BeautifulSoup


class PhotoFactory(factory.django.DjangoModelFactory):
        """User factory for testing."""

        class Meta:
            """Model meta."""

            model = Photo

        # owner = billy
        title = factory.Sequence(lambda n: "photo{}".format(n))
        photo = 'imager_images/static/generic.jpg'


class AlbumFactory(factory.django.DjangoModelFactory):
        """User factory for testing."""

        class Meta:
            """Model meta."""

            model = Album

        title = factory.Sequence(lambda n: "album{}".format(n))


class PhotoAlbumBackendTests(TestCase):
    """The Profile Model test runner for db stuff."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.client = Client()
        self.request = RequestFactory()
        self.users = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]
        self.albums = [AlbumFactory.create() for i in range(20)]

    def add_test_user(self):
        """Make test user and return his profile."""
        user = UserFactory.create()
        user.username = 'BillyTheGoat'
        user.set_password('billyspassword')
        photo = PhotoFactory.create()
        photo.owner = user.profile
        user.save()
        photo.save()
        return user

    # def test_can_add_photos_to_album(self):
    #     """Photo can be associated with albums."""
    #     photo = self.photos[0]
    #     album = AlbumFactory()
    #     album.owner = photo.owner
    #     album.photos.add(photo)
    #     album.save()
    #     self.assertTrue(album.photos.first() is photo)

    def test_library_route_is_status_ok(self):
        """Test that library view status code is 200."""
        from imager_images.views import LibraryView
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("library"))
        request.user = test_user
        view = LibraryView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_library_view_uses_correct_template(self):
        """Test that library view uses the correct template."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.client.get("/images/library/")
        request.user = test_user
        self.assertTemplateUsed(request, 'imager_images/library.html')

    def test_album_gallery_route_is_status_ok(self):
        """Test that album gallery view status code is 200."""
        from imager_images.views import AlbumGalleryView
        request = self.request.get(reverse_lazy("album_gallery"))
        view = AlbumGalleryView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_album_gallery_uses_correct_template(self):
        """Test that album gallery view uses the correct template."""
        request = self.client.get("/images/albums/")
        self.assertTemplateUsed(request, 'imager_images/album_gallery.html')

    def test_photo_gallery_route_is_status_ok(self):
        """Test that photo gallery view status code is 200t."""
        from imager_images.views import PhotoGalleryView
        request = self.request.get(reverse_lazy("photo_gallery"))
        view = PhotoGalleryView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_photo_gallery_uses_correct_template(self):
        """Test that photo gallery view uses the correct template."""
        request = self.client.get("/images/photos/")
        self.assertTemplateUsed(request, 'imager_images/photo_gallery.html')

    def test_add_photo_route_is_status_ok(self):
        """Test that add photo view status code is 200."""
        from imager_images.views import AddPhotoView
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("add_photo"))
        request.user = test_user
        view = AddPhotoView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_add_photo_view_uses_correct_template(self):
        """Test that add photo view uses the correct template."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.client.get("/images/photos/add/")
        request.user = test_user
        self.assertTemplateUsed(request, 'imager_images/add_photo.html')

    def test_add_album_route_is_status_ok(self):
        """Test that add album view status code is 200."""
        from imager_images.views import AddAlbumView
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.request.get(reverse_lazy("add_album"))
        request.user = test_user
        view = AddAlbumView.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_add_album_view_uses_correct_template(self):
        """Test that add album view uses the correct template."""
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.client.get("/images/albums/add/")
        request.user = test_user
        self.assertTemplateUsed(request, 'imager_images/add_album.html')

    def test_photo_view_is_status_ok(self):
        """Test that photo view status code is 200."""
        photo = self.photos[0]
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        response = self.client.get("/images/photos/" + str(photo.id), follow=True)
        self.assertTrue(response.status_code == 200)

    def test_photo_view_uses_correct_template(self):
        """Test that photo view uses the correct template."""
        photo = self.photos[0]
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        request = self.client.get("/images/photos/" + str(photo.id), follow=True)
        request.user = test_user
        self.assertTemplateUsed(request, 'imager_images/photo.html')

    def test_edit_photo_view_is_status_ok(self):
        """Test that photo view status code is 200."""
        photo = self.photos[0]
        test_user = self.add_test_user()
        photo.owner = test_user.profile
        photo.save()
        self.client.force_login(test_user)
        request = self.client.get("/images/photos/" + str(photo.pk) + "/edit/", follow=True)
        self.assertTrue(request.status_code == 200)

    def test_edit_photo_view_uses_correct_template(self):
        """Test that edit photo view uses the correct template."""
        photo = self.photos[0]
        test_user = self.add_test_user()
        photo.owner = test_user.profile
        photo.save()
        self.client.force_login(test_user)
        request = self.client.get("/images/photos/" + str(photo.id) + "/edit/", follow=True)
        request.user = test_user
        self.assertTemplateUsed(request, 'imager_images/edit_photo.html')

    def test_album_view_is_status_ok(self):
        """Test that album view status code is 200."""
        album = self.albums[0]
        album.published = 'PUBLIC'
        album.save()
        test_user = self.add_test_user()
        self.client.force_login(test_user)
        response = self.client.get("/images/albums/" + str(album.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # def test_album_view_is_forbidden_when_not_public(self):
    #     """Test that album view status code is 200."""
    #     album = self.albums[0]
    #     album.save()
    #     test_user = self.add_test_user()
    #     self.client.force_login(test_user)
    #     response = self.client.get("/images/albums/" + str(album.id), follow=True)
    #     self.assertTrue(response.status_code == 403)

    def test_edit_album_view_is_status_ok(self):
        """Test that album view status code is 200."""
        album = self.albums[0]
        test_user = self.add_test_user()
        album.owner = test_user.profile
        album.save()
        self.client.force_login(test_user)
        response = self.client.get("/images/albums/" + str(album.id) + "/edit", follow=True)
        self.assertTrue(response.status_code == 200)

    def test_edit_album_view_uses_correct_template(self):
        """Test that edit album view status code is 200."""
        album = self.albums[0]
        test_user = self.add_test_user()
        album.owner = test_user.profile
        album.save()
        self.client.force_login(test_user)
        response = self.client.get("/images/albums/" + str(album.id) + "/edit", follow=True)
        self.assertTemplateUsed(response, 'imager_images/edit_album.html')

    # def test_logged_in_user_can_get_to_edit_photo_page(self):
    #     """Test authenticated user can get to edit photo page."""
    #     photo = self.photos[0]
    #     user = self.user_login()
    #     self.client.force_login(user)
    #     response = self.client.get("/images/photos/" + str(photo.pk) + "/edit/")
    #     self.assertTrue(response.status_code == 200)