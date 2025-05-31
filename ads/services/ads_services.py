from ..models import *


class AdsService:
    def __init__(self):
        self.Ad = Ad.objects
        self.Category = Category.objects
        self.Condition = Condition.objects
        self.User = User.objects

    def create_ad(self, username, data):
        try:
            title = data.get('title')
            description = data.get('description')
            category_name = data.get('category')
            condition_name = data.get('condition')

            if not all([username, title, description, category_name, condition_name]):
                return {'is_created': False,
                        'message': 'Send all required fields (username, title, description, category, condition)'}

            if not self.Category.filter(name=category_name).exists():
                return {'is_created': False, 'message': f'Invalid category: {category_name}'}

            if not self.Condition.filter(name=condition_name).exists():
                return {'is_created': False, 'message': f'Invalid condition: {condition_name}'}

            user_obj = self.User.get(username=username)
            category_obj = self.Category.get(name=category_name)
            condition_obj = self.Condition.get(name=condition_name)
            self.Ad.create(user=user_obj, title=title, description=description,
                           category=category_obj, condition=condition_obj)

            return {'is_created': True,
                    'message': f'Ad created successfully ({username}, {title}, {category_name}, {condition_name})'}
        except Exception as e:
            return {'is_created': False, 'message': str(e)}

    def delete_ad(self, username, data):
        try:
            ad_id = data.get('ad_id')

            if not ad_id:
                return {'is_deleted': False,
                        'message': 'Send all required fields (username, ad_id)'}

            if not self.User.filter(username=username).exists():
                return {'is_deleted': False, 'message': f'Invalid username (now: {username})'}

            user_obj = self.User.get(username=username)
            if not self.Ad.filter(id=ad_id, user=user_obj).exists():
                return {'is_deleted': False,
                        'message': 'Ad with ID "{ad_id}" does not exist or does not belong to the user'}

            self.Ad.filter(id=ad_id, user=user_obj).delete()

            return {'is_deleted': True, 'message': 'Ad successfully deleted'}
        except Exception as e:
            return {'is_deleted': False, 'message': str(e)}

    def edit_ad(self, username, data):
        try:
            ad_id = data.get('ad_id')
            title = data.get('title')
            description = data.get('description')
            category_name = data.get('category')
            condition_name = data.get('condition')

            if not ad_id:
                return {'is_edited': False,
                        'message': 'Send all required fields (username, ad_id)'}

            if not self.User.filter(username=username).exists():
                return {'is_edited': False, 'message': f'Invalid username (now: {username})'}

            user_obj = self.User.get(username=username)
            if not self.Ad.filter(id=ad_id, user=user_obj).exists():
                return {'is_edited': False,
                        'message': f'Ad with ID "{ad_id}" does not exist or does not belong to the user'}

            if not self.Category.filter(name=category_name).exists():
                return {'is_edited': False, 'message': f'Invalid category: {category_name}'}

            if not self.Condition.filter(name=condition_name).exists():
                return {'is_edited': False, 'message': f'Invalid condition: {condition_name}'}

            category_obj = self.Category.get(name=category_name)
            condition_obj = self.Condition.get(name=condition_name)

            ad_obj = self.Ad.get(id=ad_id, user=user_obj)
            ad_obj.title = title
            ad_obj.description = description
            ad_obj.category = category_obj
            ad_obj.condition = condition_obj

            ad_obj.save()
            return {'is_edited': True,
                    'message': 'Ad edited successfully ({username}, {title}, {category_name}, {condition_name})'}
        except Exception as e:
            return {'is_edited': False, 'message': str(e)}
