from flask import url_for, request, session
from flask_admin import BaseView, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from markupsafe import Markup
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from wtforms import TextAreaField, PasswordField, TextField
from wtforms.ext.csrf import SecureForm
from wtforms.widgets import TextArea
from flask_admin import form

# https://stackoverflow.com/questions/34971368/getting-ckeditor-to-work-with-flask-admin
import settings


class CKEditorWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKEditorWidget, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditorWidget()


class SecuredHomeView(AdminIndexView):

    def __init__(self):
        super(SecuredHomeView, self).__init__(template='admin/index.html', url='/admin')

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')
        return redirect(url_for('security.login', next=request.full_path))


class MySecureForm(SecureForm):
    def generate_csrf_token(self, csrf_context):
        if '_csrf_token' not in session:
            import os, binascii
            session['_csrf_token'] = binascii.b2a_hex(os.urandom(15))
        return session['_csrf_token']


class AdminOnlyModelView(ModelView):
    # form_base_class = MySecureForm
    for_admin_only = True



    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')
        return redirect(url_for('security.login', next=request.full_path))


# https://stackoverflow.com/questions/28970076/how-to-use-flask-admin-for-editing-modelview#_=_
class SafePasswordField(TextField):
    def process_data(self, value):
        self.data = ''  # even if password is already set, don't show hash here
        # or else it will be double-hashed on save
        self.orig_hash = value

    def process_fromdata(self, valuelist):
        value = ''
        if valuelist:
            value = valuelist[0]
        if value:
            self.data = generate_password_hash(value)
        else:
            self.data = self.orig_hash


class PageModelView(AdminOnlyModelView):
    column_list= ('title', 'tag', 'keyword', 'view_count', 'stamp')
    column_sortable_list = ['view_count', 'stamp']
    column_searchable_list = ['title', 'tag']
    column_default_sort = 'stamp'

    form_columns = ['title', 'category', 'tag', 'feature_image', 'feature_image_external_url',
                    'feature_youtube_embed_code', 'excerpt', 'content','url', 'is_homepage', 'prev_page', 'next_page',
                    'subtype', 'pagestate', 'is_protected', 'password', 'stamp', ]
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'

    form_overrides = dict(
        password=SafePasswordField,
        content=CKEditorField,
        excerpt=CKEditorField
    )
    form_widget_args = dict(
        password=dict(
            placeholder='Masukkan password baru jika ingin merubah password lama',
        ),
    )

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.active = True
            model.pending = False

        if form.password.data:
            model.password = generate_password_hash(form.password.data.strip())

    def scaffold_form(self):
        form_class = super(PageModelView, self).scaffold_form()
        form_class.password = PasswordField('password')
        return form_class


class MenuModelView(AdminOnlyModelView):
    form_columns = ('title', 'order')


class UserModelView(AdminOnlyModelView):
    column_list = ('email', 'phone', 'active', 'roles')
    form_columns = ('email', 'phone', 'active', 'roles')


class RoleModelView(AdminOnlyModelView):
    pass


class SiteConfigurationView(AdminOnlyModelView):
    pass


class ImageView(AdminOnlyModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        url = '/static/upload/' + form.thumbgen_filename(model.path)
        return Markup('<a href="{}" target="_blank"><img src="{}"></a>'.format(url, url))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=settings.FILE_PATH,
                                      thumbnail_size=(100, 100, True))
    }