from graphene import AbstractType, Field


def get_viewer_node():
    from danesh_boom.schema import ViewerNode
    return ViewerNode


class ViewerFields(AbstractType):
    viewer = Field(get_viewer_node)

    def resolve_viewer(self, args, context, info):
        from danesh_boom.schema import ViewerNode
        return ViewerNode(id="0")
