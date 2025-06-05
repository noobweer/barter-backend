from rest_framework import status

from ..models import *


class ExchangeService:
    def __init__(self):
        self.Ad = Ad.objects
        self.Category = Category.objects
        self.Condition = Condition.objects
        self.User = User.objects
        self.ExchangeProposal = ExchangeProposal.objects

    def create_exchange(self, data):
        try:
            ad_sender_id = data.get('ad_sender_id')
            ad_receiver_id = data.get('ad_receiver_id')
            comment = data.get('comment')

            if not all([ad_sender_id, ad_receiver_id]):
                return {'is_created': False, 'message': 'Send all required fields (ad_sender_id, ad_receiver_id)'}

            if ad_sender_id == ad_receiver_id:
                return {'is_created': False, 'message': 'You cant exchange with yourself'}

            if not self.Ad.filter(id=ad_sender_id).exists():
                return {'is_created': False, 'message': f'Invalid ad_sender_id ({ad_sender_id})'}

            if not self.Ad.filter(id=ad_receiver_id).exists():
                return {'is_created': False, 'message': f'Invalid ad_receiver_id ({ad_receiver_id})'}

            ad_sender_obj = self.Ad.get(id=ad_sender_id)
            ad_receiver_obj = self.Ad.get(id=ad_receiver_id)
            self.ExchangeProposal.create(ad_sender=ad_sender_obj, ad_receiver=ad_receiver_obj, comment=comment)

            return {'is_created': True, 'message': f'Ad created successfully ({ad_sender_id}, {ad_receiver_id}, {comment})'}
        except Exception as e:
            return {'is_created': False, 'message': str(e)}

    def edit_exchange(self, username, data):
        try:
            exchange_id = data.get('exchange_id')
            exchange_status = data.get('status')

            if not all([exchange_id, exchange_status]):
                return {'is_edited': False, 'message': 'Send all required fields (exchange_id, status)'}

            if not self.ExchangeProposal.filter(id=exchange_id).exists():
                return {'is_edited': False, 'message': f'Invalid exchange_id ({exchange_id})'}

            if not (self.ExchangeProposal.filter(ad_sender__user__username=username).exists() or self.ExchangeProposal.filter(ad_receiver__user__username=username).exists()):
                return {'is_edited': False,
                        'message': f'Exchange with ID "{exchange_id}" does not exist or does not belong to you'}

            if exchange_status not in ['pending', 'accepted', 'declined', 'Ожидает', 'Принято', 'Отклонено']:
                return {'is_edited': False, 'message': f'Invalid exchanges status ({exchange_id}, {exchange_status})'}

            exchange_obj = self.ExchangeProposal.get(id=exchange_id)
            exchange_obj.status = exchange_status
            exchange_obj.save()

            return {'is_edited': True, 'message': f'Exchange edited successfully ({exchange_status})'}
        except Exception as e:
            return {'is_edited': False, 'message': str(e)}

    def all_exchanges(self, data):
        try:
            sender_username = data.get('sender_username')
            receiver_username = data.get('receiver_username')
            exchange_status = data.get('status', [])

            result = self.ExchangeProposal.all()

            if sender_username:
                if not self.User.filter(username=sender_username).exists():
                    return status.HTTP_400_BAD_REQUEST
                result = result.filter(ad_sender__user__username=sender_username)

            if receiver_username:
                if not self.User.filter(username=receiver_username).exists():
                    return status.HTTP_400_BAD_REQUEST
                result = result.filter(ad_receiver__user__username=receiver_username)

            if exchange_status:
                result = result.filter(status__in=exchange_status)

            return result
        except Exception as e:
            print(e)
            return status.HTTP_400_BAD_REQUEST
