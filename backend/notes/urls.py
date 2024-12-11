from rest_framework_nested import routers

from .views import TopicViewSet, NoteViewSet

router = routers.DefaultRouter()
router.register('topics', TopicViewSet, basename='topics')

topic_router = routers.NestedDefaultRouter(router, 'topics', lookup='topic')
topic_router.register('notes', NoteViewSet, basename='topic-notes')

urlpatterns = router.urls + topic_router.urls