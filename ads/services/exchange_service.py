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

            if not self.Ad.filter(id=ad_sender_id).exists():
                return {'is_create': False, 'message': f'Invalid ad_sender_id ({ad_sender_id})'}

            if not self.Ad.filter(id=ad_receiver_id).exists():
                return {'is_create': False, 'message': f'Invalid ad_receiver_id ({ad_receiver_id})'}

            ad_sender_obj = self.Ad.filter(id=ad_sender_id)
            ad_receiver_obj = self.Ad.filter(id=ad_receiver_id)
            self.ExchangeProposal.create(ad_sender=ad_sender_obj, ad_receiver=ad_receiver_obj, comment=comment)

            return {'is_created': True, 'message': f'Ad created successfully ({ad_sender_id}, {ad_receiver_id}, {comment})'}
        except Exception as e:
            return {'is_created': False, 'message': str(e)}

    def edit_exchange(self, data):
        try:
            exchange_id = data.get('exchange_id')
            status = data.get('status')

            if not all([exchange_id, status]):
                return {'is_edited': False, 'message': 'Send all required fields (exchange_id, status)'}

            if not self.ExchangeProposal.filter(id=exchange_id).exists():
                return {'is_edited': False, 'message': f'Invalid exchange_id ({exchange_id})'}

            exchange_obj = self.ExchangeProposal.get(id=exchange_id)
            exchange_obj.status = status
            exchange_obj.save()

            return {'is_edited': True, 'message': f'Exchange edited successfully ({status})'}
        except Exception as e:
            return {'is_edited': False, 'message': str(e)}
