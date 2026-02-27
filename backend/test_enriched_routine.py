#!/usr/bin/env python
from skincare_routine import get_complete_routine, enrich_routine_with_products
import json

# Test with sample products from XLSX
products = [
    {'product': 'CeraVe Foaming Cleanser', 'description': 'Gentle foaming cleanser', 'price': '₹1800-2200', 'ingredients': 'Salicylic Acid, Zinc', 'concern': 'acne'},
    {'product': 'The Ordinary Niacinamide Serum', 'description': 'Lightweight serum', 'price': '₹500-600', 'ingredients': 'Niacinamide, Squalane', 'concern': 'acne'},
    {'product': 'CeraVe Moisturizing Cream', 'description': 'Rich hydrating cream', 'price': '₹800-1000', 'ingredients': 'Ceramides, Hyaluronic Acid', 'concern': 'dryness'}
]

routine = get_complete_routine('Oily')
enriched = enrich_routine_with_products(routine, products)

print('✅ Routine enriched with products!')
print('\n🌅 Morning Routine:')
for step in enriched['morning']['steps']:
    print(f"\n  Step {step.get('step_number')}: {step.get('name')}")
    print(f"  Description: {step.get('description')}")
    if step.get('recommended_product'):
        prod = step['recommended_product']
        print(f"  ✨ Recommended: {prod['product']}")
        print(f"     Price: {prod['price']}")
        print(f"     Ingredients: {prod['ingredients']}")
