import pandas as pd
import requests


df = pd.read_csv('C:/Users/Documents/MailPOShared.csv')


API_KEY = ''

#Query Google API
def get_place_details(store_name, address):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': f'{store_name}, {address}',
        'inputtype': 'textquery',
        'fields': 'place_id,business_status,formatted_address,types',
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    place_data = response.json()
    
    if place_data['status'] == 'OK':
        place_info = place_data['candidates'][0]
        return {
            'place_id': place_info.get('place_id'),
            'business_status': place_info.get('business_status'),
            'formatted_address': place_info.get('formatted_address'),
            'types': place_info.get('types')
        }
    else:
        return None


df['query'] = df.apply(lambda x: get_place_details(x['Store Name'], f"{x['street']}, {x['city']}, {x['state']}, {x['zip']}"), axis=1)


df['business_status'] = df['query'].apply(lambda x: x['business_status'] if x else 'Unknown')
df['types'] = df['query'].apply(lambda x: ', '.join(x['types']) if x else 'Unknown')
df['formatted_address'] = df['query'].apply(lambda x: x['formatted_address'] if x else 'Unknown')


df.to_csv('business_statuses.csv', index=False)

print("Business status and types saved to business_statuses.csv")

# Notes from the Google Places API on what terms mean:
    
# Business Statuses # Notes & Definitions # Not Completely Correct yet

# OPERATIONAL:
# The business is currently open and operational. This is the default status for active businesses.

# CLOSED_TEMPORARILY:
# The business is temporarily closed. This could be due to renovations, seasonal closure, or other temporary circumstances.

# CLOSED_PERMANENTLY:
# The business has permanently closed and is no longer operational at the given location.

# Business Types
# The types field is a list of classifications that describe the nature of the place. Here are some common types:

# store:
# General term for retail businesses. You might see this for various types of shops.

# restaurant:
# Indicates a place where food and drinks are served. This covers all types of dining establishments.

# lodging:
# Refers to accommodations like hotels, motels, or inns.

# point_of_interest:
# A broad category that can encompass any notable location, including businesses, landmarks, or tourist attractions.

# establishment:
# A generic type that refers to any kind of business or place that serves a commercial purpose.

# residential:
# Indicates that the place is a residential area or home, not a commercial business.

# finance, bank:
# Types related to financial institutions like banks, ATMs, or investment firms.

# online_only:
# If a business operates exclusively online and doesn't have a physical storefront

# real_estate_agency:
# Indicates that the business is a real estate agency.

# health, doctor, pharmacy:
# Types related to healthcare services, including hospitals, clinics, and pharmacies.

# shopping_mall, department_store:
# Types associated with large retail complexes or department stores.

# school, university:
# Educational institutions.

# church, place_of_worship:
# Religious institutions.

# supermarket:
# Indicates large grocery stores or supermarkets.
