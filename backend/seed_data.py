"""
Seed script — run: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from listings.models import Property, Amenity
from agents.models import Agent
from decimal import Decimal

User = get_user_model()

PROPERTIES = [
    {'title': 'Modern 3BR Apartment in Kiyovu', 'description': 'Beautiful modern apartment in Kiyovu, Kigali.', 'purpose': 'sale', 'property_type': 'apartment', 'furnishing_status': 'furnished', 'province': 'Kigali', 'city': 'Kigali', 'area': 'Kiyovu', 'full_address': 'KN 5 Rd, Kiyovu, Kigali', 'latitude': Decimal('-1.9506'), 'longitude': Decimal('29.8747'), 'bedrooms': 3, 'bathrooms': 2, 'built_up_area': Decimal('145'), 'price': Decimal('185000000'), 'is_price_negotiable': True, 'year_built': 2023, 'parking_spaces': 2, 'is_gated_community': True, 'has_power_backup': True, 'has_lift': True, 'listing_status': 'active', 'verification_status': 'verified', 'agent_name': 'Jean-Pierre Mugabo', 'agent_phone': '+250788123456', 'is_agent_verified': True, 'views_count': 245, 'favorites_count': 32, 'rating': Decimal('4.5')},
    {'title': 'Luxury Villa in Kimihurura', 'description': 'Stunning 5BR villa with garden and pool.', 'purpose': 'sale', 'property_type': 'villa', 'furnishing_status': 'furnished', 'province': 'Kigali', 'city': 'Kigali', 'area': 'Kimihurura', 'full_address': 'KG 7 Ave, Kimihurura', 'latitude': Decimal('-1.9441'), 'longitude': Decimal('29.8731'), 'bedrooms': 5, 'bathrooms': 4, 'built_up_area': Decimal('350'), 'plot_area': Decimal('800'), 'price': Decimal('450000000'), 'is_price_negotiable': True, 'year_built': 2022, 'parking_spaces': 3, 'is_gated_community': True, 'has_power_backup': True, 'has_lift': False, 'listing_status': 'featured', 'verification_status': 'verified', 'agent_name': 'Marie Claire Uwimana', 'agent_phone': '+250788987654', 'is_agent_verified': True, 'views_count': 520, 'favorites_count': 67, 'rating': Decimal('4.8')},
    {'title': 'Affordable 2BR in Remera', 'description': 'Spacious 2BR near shops and transport.', 'purpose': 'rent', 'property_type': 'apartment', 'furnishing_status': 'semi-furnished', 'province': 'Kigali', 'city': 'Kigali', 'area': 'Remera', 'full_address': 'KG 15 Ave, Remera', 'latitude': Decimal('-1.9537'), 'longitude': Decimal('30.0914'), 'bedrooms': 2, 'bathrooms': 1, 'built_up_area': Decimal('85'), 'price': Decimal('350000'), 'is_price_negotiable': False, 'year_built': 2020, 'parking_spaces': 1, 'is_gated_community': True, 'has_power_backup': True, 'has_lift': True, 'listing_status': 'active', 'verification_status': 'verified', 'agent_name': 'Patrick Habimana', 'agent_phone': '+250788111222', 'is_agent_verified': True, 'views_count': 180, 'favorites_count': 25, 'rating': Decimal('4.2')},
    {'title': 'Commercial Space in Nyarugenge', 'description': 'Prime commercial space in business district.', 'purpose': 'rent', 'property_type': 'commercial', 'furnishing_status': 'unfurnished', 'province': 'Kigali', 'city': 'Kigali', 'area': 'Nyarugenge', 'full_address': 'KN 2 Ave, Nyarugenge', 'latitude': Decimal('-1.9530'), 'longitude': Decimal('30.0589'), 'bedrooms': None, 'bathrooms': 2, 'built_up_area': Decimal('200'), 'price': Decimal('800000'), 'is_price_negotiable': True, 'year_built': 2019, 'parking_spaces': 5, 'is_gated_community': False, 'has_power_backup': True, 'has_lift': False, 'listing_status': 'active', 'verification_status': 'verified', 'agent_name': 'Diane Mukamana', 'agent_phone': '+250788333444', 'is_agent_verified': True, 'views_count': 95, 'favorites_count': 12, 'rating': Decimal('4.0')},
    {'title': 'Land Plot in Musanze', 'description': 'Beautiful land near Volcanoes National Park.', 'purpose': 'sale', 'property_type': 'land', 'province': 'Northern', 'city': 'Musanze', 'area': 'Kinigi', 'full_address': 'Kinigi, Musanze', 'latitude': Decimal('-1.4775'), 'longitude': Decimal('29.5446'), 'plot_area': Decimal('5000'), 'price': Decimal('25000000'), 'is_price_negotiable': True, 'parking_spaces': 0, 'is_gated_community': False, 'has_power_backup': False, 'has_lift': False, 'listing_status': 'active', 'verification_status': 'verified', 'agent_name': 'Emmanuel Niyonzima', 'agent_phone': '+250788555666', 'is_agent_verified': False, 'views_count': 130, 'favorites_count': 18, 'rating': Decimal('3.8')},
]

class Command(BaseCommand):
    help = 'Seed database with sample Rwanda property data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding...')
        users_data = [
            ('admin', 'admin@rwandaestate.rw', 'Admin', 'User', 'Kigali', '+250788000000', 'admin'),
            ('jp_mugabo', 'jean@rwandaestate.rw', 'Jean-Pierre', 'Mugabo', 'Kigali', '+250788123456', 'agent'),
            ('mc_uwimana', 'marie@rwandaestate.rw', 'Marie Claire', 'Uwimana', 'Kigali', '+250788987654', 'agent'),
            ('p_habimana', 'patrick@rwandaestate.rw', 'Patrick', 'Habimana', 'Kigali', '+250788111222', 'agent'),
            ('buyer_john', 'john@buyer.rw', 'John', 'Doe', 'Kigali', '+250788123000', 'buyer'),
        ]
        users = {}
        for username, email, first, last, province, phone, role in users_data:
            user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'first_name': first, 'last_name': last, 'phone': phone, 'role': role, 'preferred_language': 'en'})
            if created:
                user.set_password('password123')
                user.save()
                UserProfile.objects.get_or_create(user=user, defaults={'province': province})
            users[username] = user
            self.stdout.write(f'  ✅ User: {username}')

        amenities = [(1, '24/7 Security', 'shield-check', 'security'), (2, 'CCTV', 'cctv', 'security'), (3, 'Parking', 'car', 'parking'), (4, 'Gym', 'dumbbell', 'recreation'), (5, 'Swimming Pool', 'pool', 'recreation'), (6, 'Garden', 'tree', 'recreation'), (7, 'Power Backup', 'lightning-bolt', 'utilities'), (8, 'Water Supply', 'water', 'utilities'), (9, 'Internet', 'wifi', 'utilities'), (10, 'Lift/Elevator', 'elevator', 'utilities'), (11, 'Playground', 'baby-carriage', 'recreation'), (12, 'Gated Community', 'gate', 'security')]
        for aid, name, icon, category in amenities:
            Amenity.objects.get_or_create(id=aid, defaults={'name': name, 'icon': icon, 'category': category})

        agent_map = {'Jean-Pierre Mugabo': users['jp_mugabo'], 'Marie Claire Uwimana': users['mc_uwimana'], 'Patrick Habimana': users['p_habimana'], 'Diane Mukamana': users.get('diane', users['jp_mugabo']), 'Emmanuel Niyonzima': users.get('emmanuel', users['p_habimana'])}
        for prop_data in PROPERTIES:
            agent_name = prop_data.pop('agent_name')
            owner = agent_map.get(agent_name, users['admin'])
            Property.objects.create(owner=owner, **prop_data)
            self.stdout.write(f'  ✅ Property: {prop_data["title"]}')

        agents_data = [('jp_mugabo', 'Kigali', True, True, 4.7, 45), ('mc_uwimana', 'Kigali', True, True, 4.9, 62), ('p_habimana', 'Kigali', True, False, 4.3, 28)]
        for username, province, is_verified, is_featured, rating, count in agents_data:
            user = users[username]
            Agent.objects.get_or_create(user=user, defaults={'province': province, 'is_verified': is_verified, 'is_featured': is_featured, 'rating': Decimal(str(rating)), 'properties_count': count, 'response_rate': Decimal('85.5'), 'bio': f'Experienced agent in {province}', 'company_name': 'Rwanda Estate Realty', 'years_of_experience': 5})

        self.stdout.write('\n🎉 Done!')
        self.stdout.write('📝 admin / password123')
        self.stdout.write('📝 buyer_john / password123')
        self.stdout.write('📝 jp_mugabo / password123')

