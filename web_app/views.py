from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField
from wtforms.widgets import TextArea

# https://stackoverflow.com/questions/34971368/getting-ckeditor-to-work-with-flask-admin
class CKEditorWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKEditorWidget, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditorWidget()


class PageModelView(ModelView):
    column_list= ('title', 'tag', 'keyword')
    form_overrides = dict(content=CKEditorField)
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'


class MenuModelView(ModelView):
    form_columns = ('title', 'order', 'page')