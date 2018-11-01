import json

from django.db.models import Q
from django.core import serializers
from requests.status_codes import title
from rest_framework import status
from rest_framework.decorators import list_route, detail_route
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .permissions import (
    IsRollOwnerOrReadOnly,
    IsRollPermissionOwnerOrReadOnly,
    IsAdminUserOrReadOnly,
    IsHashtagOwnerOrReadOnly,
    IsCommentOwnerOrReadOnly,
    IsBadgeCategoryOwnerOrReadOnly,
    BadgePermission,
    CanReadBadge,
)

from .models import (
    Base,
    Hashtag,
    HashtagParent,
    BaseComment,
    Post,
    BaseCertificate,
    BaseRoll,
    RollPermission,
    HashtagRelation,
    BaseCountry,
    BaseProvince,
    BaseTown,
    BadgeCategory,
    Badge,
    Favorite)

from .serializers import (
    BaseSerializer,
    HashtagSerializer,
    HashtagParentSerializer,
    BaseCommentSerializer,
    BaseCommentListSerializer,
    PostSerializer,
    PostListSerializer,
    CertificateSerializer,
    CertificateListSerializer,
    RollSerializer,
    RollPermissionSerializer,
    HashtagRelationSerializer,
    BaseCountrySerializer,
    BaseProvinceSerializer,
    BaseTownSerializer,
    BadgeCategorySerializer,
    BadgeCategoryListSerializer,
    BadgeSerializer,
    BadgeListSerializer,
    FavoriteSerializer, FavoriteListSerializer)


class BaseModelViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        """class DynamicDeleteSerializer(ModelSerializer, BaseSerializer):
            class Meta:
                model = self.get_serializer_class().Meta.model
                fields = []

            def validate(self, attrs):
                if self.instance.delete_flag:
                    raise ValidationError('Ths selected object does not exist or already deleted.')
                return attrs"""

        try:
            instance = self.get_object()
            # serializer = DynamicDeleteSerializer(instance, request.data)
            # serializer.is_valid(raise_exception=True)
            instance.delete_flag = True
            instance.save()
            # return Response({status: "SUCCESS"}, status=status.HTTP_200_OK)
            response = HttpResponse(json.dumps({'message': 'record deleted.'}), content_type='application/json')
            response.status_code = 200
            return response
        except Exception as e:
            if type(e) is ValidationError:
                raise e

        return Response({
            "errors": [{
                "status": 1,
                "key": "non_field_errors",
                "detail": "The selected object does not exist or already deleted."
            }]
        }, status=status.HTTP_404_NOT_FOUND)


class BaseViewset(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = Base.objects.all()
        child_name = self.request.query_params.get('child_name', None)
        if child_name is not None:
            queryset = queryset.filter(child_name=child_name)
        return queryset

    def get_serializer_class(self):
        return BaseSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class HashtagParentViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = HashtagParent.objects.filter(delete_flag=False)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return HashtagParentSerializer

    @list_route(methods=['post'], permission_classes=[IsAdminUser])
    def import_hashtags(self, request):
        jsonString = request.data.get('records', None)
        if jsonString is not None:
            data = json.loads(jsonString)
            errors = []
            # Add Hashtags First
            for record in data:
                if record.get('title', None) is not None:
                    hashtag_count = HashtagParent.objects.filter(title=record.get('title', None)).count()
                    print(record.get('title', None))
                    if hashtag_count == 0:
                        print('is zero')
                        try:
                            hashtag_object = HashtagParent.objects.create(title=record.get('title', None))
                        except Exception as e:
                            errors.append({
                                'data': record,
                                'status': str(e)
                            })
                    else:
                        print('is not zero')
                else:
                    errors.append({
                        'data': record,
                        'status': 'this record have not title'
                    })
            # Add Hashtag Relations
            for record in data:
                if record.get('title', None) is not None:
                    try:
                        hashtag = HashtagParent.objects.get(title=record.get('title', None))
                    except HashtagParent.DoesNotExist:
                        errors.append({
                            'data': record,
                            'status': 'hashtag not exist for set relation'
                        })
                        hashtag = None
                    if hashtag is not None:
                        hashtag_parent_id = record.get('parent_id', None)
                        if hashtag_parent_id is not None and hashtag_parent_id != '':
                            for parent_record in data:
                                if parent_record.get('title', None) is not None:
                                    if parent_record.get('id', None) == hashtag_parent_id:
                                        try:
                                            hashtag_parent_object = HashtagParent.objects.get(
                                                title=parent_record.get('title', None)
                                            )
                                        except HashtagParent.DoesNotExist:
                                            hashtag_parent_object = None
                                        if hashtag_parent_object is not None:
                                            hashtag_relation_count = HashtagRelation.objects.filter(
                                                Q(hashtag_first=hashtag, hashtag_second=hashtag_parent_object) |
                                                Q(hashtag_first=hashtag_parent_object, hashtag_second=hashtag)).count()
                                            if hashtag_relation_count == 0:
                                                try:
                                                    hashtag_realtion_object = HashtagRelation.objects.create(
                                                        hashtag_first=hashtag_parent_object,
                                                        hashtag_second=hashtag
                                                    )
                                                except Exception as e:
                                                    errors.append({
                                                        'data': record,
                                                        'status': str(e)
                                                    })
                                        else:
                                            errors.append({
                                                'data': record,
                                                'status': 'hashtag parent object not exist'
                                            })
                                        break
                    else:
                        errors.append({
                            'data': record,
                            'status': 'this record have not title'
                        })
                else:
                    errors.append({
                        'data': record,
                        'status': 'this record have not title'
                    })
        return Response(errors, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class HashtagViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsHashtagOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Hashtag.objects.filter(delete_flag=False)
        
        related_parent = self.request.query_params.get('related_parent', None)
        if related_parent is not None:
            queryset = queryset.filter(related_parent_id=related_parent)

        hashtag_title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=hashtag_title)

        hashtag_title_contain = self.request.query_params.get('title_contain', None)
        if hashtag_title_contain is not None:
            queryset = queryset.filter(title__contains=hashtag_title_contain)

        return queryset

    def get_serializer_class(self):
        return HashtagSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class HashtagRelationViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = HashtagRelation.objects.filter(delete_flag=False)

        hashtag_first = self.request.query_params.get('hashtag_first')
        if hashtag_first is not None:
            queryset = queryset.filter(hashtag_first=hashtag_first)

        hashtag_first_title = self.request.query_params.get('hashtag_first_title')
        if hashtag_first_title is not None:
            queryset = queryset.filter(hashtag_first__title=hashtag_first_title)

        hashtag_second = self.request.query_params.get('hashtag_second')
        if hashtag_second is not None:
            queryset = queryset.filter(hashtag_second=hashtag_second)

        hashtag_second_title = self.request.query_params.get('hashtag_second_title')
        if hashtag_second_title is not None:
            queryset = queryset.filter(hashtag_second__title=hashtag_second_title)

        active = self.request.query_params.get('active')
        if active is not None:
            queryset = queryset.filter(active=active)

        return queryset

    @list_route(methods=['get'], permission_classes=[IsAuthenticated])
    def search(self, request):
        relations = HashtagRelation.objects.filter(delete_flag=False)

        hashtag_text = self.request.query_params.get('hashtag_text')
        if hashtag_text is not None:
            try:
                hashtag_id = HashtagParent.objects.get(title=hashtag_text).id
            except HashtagParent.DoesNotExist:
                return []
            relations = relations.filter(Q(hashtag_first_id=hashtag_id) | Q(hashtag_second_id=hashtag_id))
            results = []
            for relation in relations:
                if relation.hashtag_first.id != hashtag_id:
                    results.append(relation.hashtag_first)
                else:
                    results.append(relation.hashtag_second)
            results_sorted = sorted(results, key=lambda x: x.usage, reverse=True)
        return Response(serializers.serialize('json', results_sorted), status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return HashtagRelationSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseCommentViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsCommentOwnerOrReadOnly]

    def get_queryset(self):
        queryset = BaseComment.objects.filter(delete_flag=False)

        comment_parent = self.request.query_params.get('comment_parent', None)
        if comment_parent is not None:
            queryset = queryset.filter(comment_parent_id=comment_parent)

        comment_sender = self.request.query_params.get('comment_sender', None)
        if comment_sender is not None:
            queryset = queryset.filter(comment_sender_id=comment_sender)
        
        text = self.request.query_params.get('text', None)
        if text is not None:
            queryset = queryset.filter(text=text)

        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BaseCommentListSerializer
        return BaseCommentSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(BaseModelViewSet):
    parent_field = 'post_parent'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(delete_flag=False).order_by('-id')

        post_type = self.request.query_params.get('post_type', None)
        if post_type is not None:
            queryset = queryset.filter(post_type=post_type)

        post_identity_id = self.request.query_params.get('post_identity_id', None)
        if post_identity_id is not None:
            queryset = queryset.filter(post_identity_id=post_identity_id)

        post_identity_name = self.request.query_params.get('post_identity_name', None)
        if post_identity_name is not None:
            queryset = queryset.filter(post_identity__name__contains=post_identity_name)

        post_related_product = self.request.query_params.get('post_related_product')
        if post_related_product is not None:
            queryset = queryset.filter(post_related_product_id=post_related_product)

        post_related_product_is_null = self.request.query_params.get('post_related_product_is_null')
        if post_related_product_is_null is not None and post_related_product_is_null == '0':
            queryset = queryset.filter(~Q(post_related_product_id=None))

        post_title = self.request.query_params.get('post_title', None)
        if post_title is not None:
            queryset = queryset.filter(post_title__contains=post_title)

        post_description = self.request.query_params.get('post_description', None)
        if post_description is not None:
            queryset = queryset.filter(post_description__contains=post_description)

        post_parent = self.request.query_params.get('post_parent', None)
        if post_parent is not None:
            queryset = queryset.filter(post_parent_id=post_parent)

        post_pinned = self.request.query_params.get('post_pinned', None)
        if post_pinned is not None:
            queryset = queryset.filter(post_pinned=post_pinned)

        return queryset

    @detail_route(
        permission_classes=[IsAuthenticated],
        methods=['get'],
        url_path='(?P<parent_id>[0-9]+)'
    )
    def count(self, request, pk=None, parent_id=None):
        post_count = Post.objects.filter(post_parent=parent_id, delete_flag=False).count()
        return Response({'count': post_count}, status=status.HTTP_200_OK)

    @detail_route(
        permission_classes=[IsAuthenticated],
        methods=['get'],
        url_path='(?P<parent_id>[0-9]+)'
    )
    def count_demand(self, request, pk=None, parent_id=None):
        post_count = Post.objects.filter(post_parent=parent_id, delete_flag=False, post_type='demand').count()
        return Response({'count': post_count}, status=status.HTTP_200_OK)

    @detail_route(
        permission_classes=[IsAuthenticated],
        methods=['get'],
        url_path='(?P<parent_id>[0-9]+)'
    )
    def count_supply(self, request, pk=None, parent_id=None):
        post_count = Post.objects.filter(post_parent=parent_id, delete_flag=False, post_type='supply').count()
        return Response({'count': post_count}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CertificateViewSet(BaseModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = BaseCertificate.objects.filter(delete_flag=False)

        certificate_parent = self.request.query_params.get('certificate_parent', None)
        if certificate_parent is not None:
            queryset = queryset.filter(certificate_parent=certificate_parent)

        certificate_identity = self.request.query_params.get('certificate_identity', None)
        if certificate_identity is not None:
            queryset = queryset.filter(certificate_identity=certificate_identity)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        return queryset

    @detail_route(
        permission_classes=[IsAuthenticated],
        methods=['get'],
        url_path='(?P<identity_id>[0-9]+)'
    )
    def count_identity(self, request, pk=None, identity_id=None):
        certificate_count = BaseCertificate.objects.filter(certificate_identity=identity_id, delete_flag=False).count()
        return Response({'count': certificate_count}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CertificateListSerializer
        return CertificateSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RollViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsRollOwnerOrReadOnly]

    def get_queryset(self):
        queryset = BaseRoll.objects.filter(delete_flag=False)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        roll_parent = self.request.query_params.get('roll_parent', None)
        if roll_parent is not None:
            queryset = queryset.filter(roll_parent=roll_parent)

        user_roll = self.request.query_params.get('user_roll', None)
        if user_roll is not None:
            queryset = queryset.filter(user_roll=user_roll)

        user_roll_username = self.request.query_params.get('user_roll_username', None)
        if user_roll_username is not None:
            queryset = queryset.filter(user_roll__username=user_roll_username)

        return queryset

    def get_serializer_class(self):
        return RollSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RollPermissionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsRollPermissionOwnerOrReadOnly]

    def get_queryset(self):
        queryset = RollPermission.objects.filter(delete_flag=False)

        roll_permission_related_roll = self.request.query_params.get('roll_permission_related_roll', None)
        if roll_permission_related_roll is not None:
            queryset = queryset.filter(roll_permission_related_roll=roll_permission_related_roll)

        roll_permission_related_roll_name = self.request.query_params.get('roll_permission_related_roll_name', None)
        if roll_permission_related_roll_name is not None:
            queryset = queryset.filter(roll_permission_related_roll__name=roll_permission_related_roll_name)

        permission = self.request.query_params.get('permission', None)
        if permission is not None:
            queryset = queryset.filter(permission=permission)

        return queryset

    def get_serializer_class(self):
        return RollPermissionSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseCountryViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = BaseCountry.objects.filter(delete_flag=False)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)

        return queryset

    def get_serializer_class(self):
        return BaseCountrySerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseProvinceViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = BaseProvince.objects.filter(delete_flag=False)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        province_related_country = self.request.query_params.get('province_related_country', None)
        if province_related_country is not None:
            queryset = queryset.filter(province_related_country=province_related_country)

        province_related_country_name = self.request.query_params.get('province_related_country_name', None)
        if province_related_country_name is not None:
            queryset = queryset.filter(province_related_country__name=province_related_country_name)

        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)

        return queryset

    def get_serializer_class(self):
        return BaseProvinceSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseTownViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = BaseTown.objects.filter(delete_flag=False)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        town_related_province = self.request.query_params.get('town_related_province', None)
        if town_related_province is not None:
            queryset = queryset.filter(town_related_province=town_related_province)

        town_related_province_name = self.request.query_params.get('town_related_province_name', None)
        if town_related_province_name is not None:
            queryset = queryset.filter(town_related_province__name=town_related_province_name)

        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)

        return queryset

    def get_serializer_class(self):
        return BaseTownSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(
        permission_classes=[IsAdminUser],
        methods=['post'])
    def import_towns(self, request):
        jsonString = request.data.get('records', None)
        country_name = request.data.get('country', None)
        data = json.loads(jsonString)
        errors = []
        if country_name is not None and jsonString is not None:
            country_count = BaseCountry.objects.filter(name=country_name).count()
            if country_count != 0:
                try:
                    country_obj = BaseCountry.objects.get(name=country_name)
                except Exception as e:
                    errors.append({
                        'data': country_name,
                        'status': str(e)
                    })
            else:
                try:
                    country_obj = BaseCountry.objects.create(name=country_name)
                except Exception as e:
                    errors.append({
                        'data': country_name,
                        'status': str(e)
                    })
        else:
            return Response({'detail': 'please insert country_name'}, status=status.HTTP_400_BAD_REQUEST)
        for record in data:
            province_count = BaseProvince.objects.filter(name=record.get('ostn_name', None),
                                                         province_related_country=country_obj).count()
            if province_count != 0:
                try:
                    province_obj = BaseProvince.objects.get(name=record.get('ostn_name', None),
                                                            province_related_country=country_obj)
                except Exception as e:
                    errors.append({
                        'data': record,
                        'status': str(e)
                    })
            else:
                try:
                    province_obj = BaseProvince.objects.create(name=record.get('ostn_name', None),
                                                               province_related_country=country_obj)
                except Exception as e:
                    errors.append({
                        'data': record,
                        'status': str(e)
                    })
            town_count = BaseTown.objects.filter(name=record.get('city_name', None),
                                                 town_related_province=province_obj).count()
            if town_count != 0:
                try:
                    town_obj = BaseTown.objects.get(name=record.get('city_name', None),
                                                    town_related_province=province_obj)
                except Exception as e:
                    errors.append({
                        'data': record,
                        'status': str(e)
                    })
            else:
                try:
                    town_obj = BaseTown.objects.create(name=record.get('city_name', None),
                                                       town_related_province=province_obj)
                except Exception as e:
                    errors.append({
                        'data': record,
                        'status': str(e)
                    })
            town_obj.save()
        response = {
            'errors': errors
        }
        return Response(response, status=status.HTTP_200_OK)


class BadgeCategoryViewSet(ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        # IsBadgeCategoryOwnerOrReadOnly
    ]

    def get_queryset(self):
        queryset = BadgeCategory.objects.filter(delete_flag=False)

        badge_title = self.request.query_params.get('badge_title', None)
        if badge_title is not None:
            queryset = queryset.filter(badge_title=badge_title)

        badge_related_media = self.request.query_params.get('badge_related_media', None)
        if badge_related_media is not None:
            queryset = queryset.filter(badge_related_media=badge_related_media)

        badge_related_user = self.request.query_params.get('badge_related_user', None)
        if badge_related_user is not None:
            queryset = queryset.filter(badge_related_user=badge_related_user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return BadgeCategoryListSerializer
        return BadgeCategorySerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BadgeViewSet(ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        BadgePermission,
        # CanReadBadge
    ]

    def get_queryset(self):
        queryset = Badge.objects.filter(delete_flag=False)

        badge_related_badge_category = self.request.query_params.get('badge_related_badge_category', None)
        if badge_related_badge_category is not None:
            queryset = queryset.filter(badge_related_badge_category=badge_related_badge_category)

        badge_related_parent = self.request.query_params.get('badge_related_parent', None)
        if badge_related_parent is not None:
            queryset = queryset.filter(badge_related_parent_id=badge_related_parent)

        badge_active = self.request.query_params.get('badge_active', None)
        if badge_active is not None:
            queryset = queryset.filter(badge_active=badge_active)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return BadgeListSerializer
        return BadgeSerializer

    @detail_route(
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='(?P<parent_id>[0-9]+)'
    )
    def parent_count(self, request, pk=None, parent_id=None):
        badge_count = Badge.objects.filter(badge_related_parent=parent_id, delete_flag=False).count()
        return Response({'count': badge_count}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return FavoriteListSerializer
        return FavoriteSerializer

    def get_queryset(self):
        queryset = Favorite.objects.filter(delete_flag=False)

        favorite_name = self.request.query_params.get('favorite_name', None)
        if favorite_name is not None:
            queryset = queryset.filter(favorite_name=favorite_name)

        favorite_related_media = self.request.query_params.get('favorite_related_media', None)
        if favorite_related_media is not None:
            queryset = queryset.filter(favorite_related_media=favorite_related_media)

        return queryset
