from import_export import resources
from .models import Blog, Blog_comment, Blog_reaction


class BlogPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = Blog
        # exclude = ('id',)
        import_id_fields = ("userid",)


class Blog_commentPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = Blog_comment
        import_id_fields = ("userid","blogid",)


class Blog_reactionPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = Blog_reaction
        # exclude = ('id',)
        import_id_fields = ("userid","blogid",)

