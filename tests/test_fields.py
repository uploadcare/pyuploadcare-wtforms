# coding: utf-8
import mock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from wtforms import Form
from pyuploadcare_wtforms.fields import (FileField, FileWidget, ImageField,
                                         FileGroupField)
from pyuploadcare.api_resources import File, FileGroup


class FakeDict(dict):
    def getlist(self, key):
        return [self[key]]


class TestForm(Form):
    file_field = FileField()


class FileFieldTestCase(unittest.TestCase):
    ucare_cdn = 'https://ucarecdn.com/ebff57dd-6f79-427b-9b43-e7109f055666/'
    form_class = TestForm
    field_name = 'file_field'
    object_type = File

    def test_widget_type(self):
        self.assertIsInstance(self.form_class()[self.field_name].widget,
                              FileWidget)

    def test_valid_form(self):
        form = self.form_class(FakeDict({self.field_name: self.ucare_cdn}))

        self.assertTrue(form.validate())
        self.assertIsInstance(form.data[self.field_name], self.object_type)

    def test_empty_form(self):
        form = self.form_class(FakeDict({}))

        self.assertTrue(form.validate())
        self.assertEqual(form.data[self.field_name], None)

    def test_invalid_value(self):
        form = self.form_class(FakeDict({self.field_name: 'invalid'}))

        self.assertFalse(form.validate())
        self.assertEqual(form.errors[self.field_name], ["Couldn't find UUID"])

    @mock.patch('pyuploadcare_wtforms.fields.conf')
    def test_render_field(self, conf):
        conf.pub_key = 'pub_key'
        conf.upload_base = 'upload_base'

        form = self.form_class()
        html = form[self.field_name]()

        self.assertTrue('data-public-key="{0}"'.format(conf.pub_key) in html)
        self.assertTrue('data-upload-base-url="{0}"'.format(conf.upload_base)
                        in html)
        self.assertTrue('role="uploadcare-uploader"'.format(conf.pub_key)
                        in html)


class ImageTestForm(Form):
    image_field = ImageField()
    image_field_cropped = ImageField(manual_crop='200x200')


class ImageFieldTestCase(FileFieldTestCase):
    form_class = ImageTestForm
    field_name = 'image_field'

    def test_render_extra_data_attributes(self):
        form = self.form_class()
        html = form[self.field_name]()

        self.assertTrue('data-images-only' in html)

    def test_manual_crop(self):
        form = self.form_class()
        field = form.image_field_cropped
        html = field()

        self.assertTrue('data-crop="{0}"'.format(field.manual_crop) in html)


class FileGroupTestForm(Form):
    file_group = FileGroupField()


class FileGroupFieldTestCase(FileFieldTestCase):
    ucare_cdn = 'https://ucarecdn.com/ebff57dd-6f79-427b-9b43-e7109f055666~1'
    form_class = FileGroupTestForm
    field_name = 'file_group'
    object_type = FileGroup

    def test_invalid_value(self):
        form = self.form_class(FakeDict({self.field_name: 'invalid'}))

        self.assertFalse(form.validate())
        self.assertEqual(form.errors[self.field_name],
                         ["Couldn't find group id"])

    def test_render_extra_data_attributes(self):
        form = self.form_class()
        html = form[self.field_name]()

        self.assertTrue('data-multiple' in html)
