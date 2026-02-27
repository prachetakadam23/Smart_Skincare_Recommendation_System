import json

# Skincare routine templates based on skin type and concerns
SKINCARE_ROUTINES = {
    "morning": {
        "Oily": {
            "step_1": {
                "name": "Cleanser",
                "description": "Use a gentle foaming cleanser to remove oil and impurities",
                "tip": "Use lukewarm water, not hot water"
            },
            "step_2": {
                "name": "Toner",
                "description": "Apply a balancing toner to control sebum",
                "tip": "Use a cotton pad to apply gently"
            },
            "step_3": {
                "name": "Serum",
                "description": "Apply lightweight serum (Niacinamide recommended for oil control)",
                "tip": "Use 2-3 drops, pat gently"
            },
            "step_4": {
                "name": "Lightweight Moisturizer",
                "description": "Use an oil-free, gel-based moisturizer",
                "tip": "Apply only where needed"
            },
            "step_5": {
                "name": "Sunscreen SPF 50",
                "description": "Always apply sunscreen as the final step",
                "tip": "Use at least 1/4 teaspoon for face"
            }
        },
        "Dry": {
            "step_1": {
                "name": "Gentle Cleanser",
                "description": "Use a hydrating cleanser without stripping natural oils",
                "tip": "Avoid foaming cleansers"
            },
            "step_2": {
                "name": "Hydrating Toner",
                "description": "Apply a hydrating toner with hyaluronic acid",
                "tip": "Spray and let it dry naturally"
            },
            "step_3": {
                "name": "Serum",
                "description": "Apply hydrating serum with hyaluronic acid",
                "tip": "Use on damp skin for better absorption"
            },
            "step_4": {
                "name": "Rich Moisturizer",
                "description": "Use a rich, hydrating moisturizer",
                "tip": "Can use face oils after moisturizer"
            },
            "step_5": {
                "name": "Sunscreen SPF 50",
                "description": "Apply hydrating sunscreen",
                "tip": "Choose mineral or hydrating formula"
            }
        },
        "Normal": {
            "step_1": {
                "name": "Gentle Cleanser",
                "description": "Use a pH-balanced gentle cleanser",
                "tip": "Apply for 30 seconds massage"
            },
            "step_2": {
                "name": "Toner",
                "description": "Apply a hydrating toner",
                "tip": "Optional but beneficial"
            },
            "step_3": {
                "name": "Serum",
                "description": "Apply a beneficial serum (Vitamin C for brightening)",
                "tip": "Use 2-3 drops"
            },
            "step_4": {
                "name": "Moisturizer",
                "description": "Apply a lightweight moisturizer",
                "tip": "Match to your current skin condition"
            },
            "step_5": {
                "name": "Sunscreen SPF 50",
                "description": "Always protect with sunscreen",
                "tip": "Reapply every 2 hours"
            }
        },
        "Combination": {
            "step_1": {
                "name": "Gentle Cleanser",
                "description": "Use a balanced cleanser suitable for mixed skin",
                "tip": "Not too stripping, not too heavy"
            },
            "step_2": {
                "name": "Balancing Toner",
                "description": "Apply a pH-balancing toner",
                "tip": "Use more on T-zone"
            },
            "step_3": {
                "name": "Lightweight Serum",
                "description": "Apply a balancing serum",
                "tip": "Target dry areas more"
            },
            "step_4": {
                "name": "Lightweight Moisturizer",
                "description": "Use a lightweight hydrating moisturizer",
                "tip": "More on cheeks, less on T-zone"
            },
            "step_5": {
                "name": "Sunscreen SPF 50",
                "description": "Apply mattifying sunscreen",
                "tip": "Choose for combination skin"
            }
        }
    },
    "evening": {
        "Oily": {
            "step_1": {
                "name": "Makeup Remover",
                "description": "Use micellar water or gentle remover",
                "tip": "Remove makeup completely"
            },
            "step_2": {
                "name": "Cleanser",
                "description": "Double cleanse with foaming cleanser",
                "tip": "Effective oil removal"
            },
            "step_3": {
                "name": "Toner",
                "description": "Apply oil-control toner",
                "tip": "Use cotton pad"
            },
            "step_4": {
                "name": "Targeted Treatment",
                "description": "Apply acne serum or salicylic acid if needed",
                "tip": "Use only on affected areas"
            },
            "step_5": {
                "name": "Lightweight Night Cream",
                "description": "Use lightweight gel-based night moisturizer",
                "tip": "Apply thin layer"
            }
        },
        "Dry": {
            "step_1": {
                "name": "Makeup Remover",
                "description": "Use oil-based or hydrating remover",
                "tip": "Gentle removal"
            },
            "step_2": {
                "name": "Gentle Cleanser",
                "description": "Hydrating cleanser",
                "tip": "Don't over-wash"
            },
            "step_3": {
                "name": "Toner",
                "description": "Hydrating toner",
                "tip": "Apply to damp skin"
            },
            "step_4": {
                "name": "Serum",
                "description": "Hydrating or treatment serum",
                "tip": "Use more generous amount"
            },
            "step_5": {
                "name": "Rich Night Cream",
                "description": "Use rich, nourishing night cream",
                "tip": "Can seal with face oil"
            }
        },
        "Normal": {
            "step_1": {
                "name": "Makeup Remover",
                "description": "Remove makeup with gentle remover",
                "tip": "Complete removal"
            },
            "step_2": {
                "name": "Cleanser",
                "description": "Gentle pH-balanced cleanser",
                "tip": "Minimal 30 seconds"
            },
            "step_3": {
                "name": "Toner",
                "description": "Hydrating toner",
                "tip": "Optional but beneficial"
            },
            "step_4": {
                "name": "Night Serum",
                "description": "Apply treatment serum (Retinol, Vitamin C)",
                "tip": "Alternate with other serums"
            },
            "step_5": {
                "name": "Night Moisturizer",
                "description": "Use a nourishing night cream",
                "tip": "Can be richer than daytime"
            }
        },
        "Combination": {
            "step_1": {
                "name": "Makeup Remover",
                "description": "Use lightweight remover",
                "tip": "Won't clog pores"
            },
            "step_2": {
                "name": "Cleanser",
                "description": "Balanced cleanser",
                "tip": "Gentle on all areas"
            },
            "step_3": {
                "name": "Toner",
                "description": "Balancing toner",
                "tip": "Use more on T-zone"
            },
            "step_4": {
                "name": "Treatment Serum",
                "description": "Targeted treatment serum",
                "tip": "Based on concerns"
            },
            "step_5": {
                "name": "Night Moisturizer",
                "description": "Lightweight night moisturizer",
                "tip": "Adjust thickness as needed"
            }
        }
    }
}

def get_routine_for_skin_type(skin_type, time_of_day="morning"):
    """Get skincare routine for a specific skin type and time of day"""
    if time_of_day not in SKINCARE_ROUTINES:
        time_of_day = "morning"
    
    if skin_type not in SKINCARE_ROUTINES[time_of_day]:
        skin_type = "Normal"
    
    routine = SKINCARE_ROUTINES[time_of_day][skin_type]
    
    # Convert to list format
    steps = []
    for i in range(1, len(routine) + 1):
        step_key = f"step_{i}"
        if step_key in routine:
            step_data = routine[step_key]
            step_data['step_number'] = str(i)
            steps.append(step_data)
    
    return {
        "time_of_day": time_of_day,
        "skin_type": skin_type,
        "steps": steps
    }

def get_complete_routine(skin_type):
    """Get morning and evening routine"""
    return {
        "morning": get_routine_for_skin_type(skin_type, "morning"),
        "evening": get_routine_for_skin_type(skin_type, "evening")
    }
def enrich_routine_with_products(routine, recommended_products):
    """
    Enrich skincare routine with recommended products
    Maps products to routine steps based on product type
    """
    enriched_routine = {
        "morning": routine["morning"].copy(),
        "evening": routine["evening"].copy()
    }
    
    # Create a mapping of step types to recommended products
    product_map = {}
    for product in recommended_products:
        product_name = product.get("product", "").lower()
        # Determine product type from name
        if "cleanser" in product_name or "wash" in product_name:
            product_map["cleanser"] = product
        elif "serum" in product_name:
            product_map["serum"] = product
        elif "moisturizer" in product_name or "cream" in product_name:
            product_map["moisturizer"] = product
        elif "toner" in product_name:
            product_map["toner"] = product
        elif "sunscreen" in product_name or "spf" in product_name:
            product_map["sunscreen"] = product
    
    # Enrich morning routine
    for step in enriched_routine["morning"]["steps"]:
        step_name = step.get("name", "").lower()
        step["recommended_product"] = None
        
        if "cleanser" in step_name:
            step["recommended_product"] = product_map.get("cleanser")
        elif "serum" in step_name:
            step["recommended_product"] = product_map.get("serum")
        elif "moisturizer" in step_name:
            step["recommended_product"] = product_map.get("moisturizer")
        elif "toner" in step_name:
            step["recommended_product"] = product_map.get("toner")
        elif "sunscreen" in step_name:
            step["recommended_product"] = product_map.get("sunscreen")
    
    # Enrich evening routine
    for step in enriched_routine["evening"]["steps"]:
        step_name = step.get("name", "").lower()
        step["recommended_product"] = None
        
        if "cleanser" in step_name:
            step["recommended_product"] = product_map.get("cleanser")
        elif "serum" in step_name:
            step["recommended_product"] = product_map.get("serum")
        elif "moisturizer" in step_name:
            step["recommended_product"] = product_map.get("moisturizer")
        elif "toner" in step_name:
            step["recommended_product"] = product_map.get("toner")
        elif "treatment" in step_name:
            step["recommended_product"] = product_map.get("serum")
    
    return enriched_routine


def get_product_specific_routine(product, skin_type="Normal"):
    """
    Create a 5-step routine specifically for ONE product.
    Each step shows how to use that specific product in different ways.
    """
    product_name = product.get("product", "Product")
    description = product.get("description", "")
    concern = product.get("concern", "")
    
    # Determine product type from description or name
    product_lower = (product_name + description).lower()
    
    if "cleanser" in product_lower or "wash" in product_lower or "foam" in product_lower:
        product_type = "Cleanser"
    elif "serum" in product_lower or "essence" in product_lower:
        product_type = "Serum"
    elif "moisturizer" in product_lower or "cream" in product_lower or "lotion" in product_lower:
        product_type = "Moisturizer"
    elif "toner" in product_lower or "mist" in product_lower:
        product_type = "Toner"
    elif "sunscreen" in product_lower or "spf" in product_lower:
        product_type = "Sunscreen"
    elif "mask" in product_lower or "pack" in product_lower:
        product_type = "Treatment"
    else:
        product_type = "Product"
    
    routine = {
        "product": product_name,
        "product_type": product_type,
        "concern": concern,
        "description": description,
        "morning": {
            "steps": [
                {
                    "step_number": "1",
                    "name": f"Cleanse",
                    "description": f"Start with your morning cleanse to prepare skin for {product_name}",
                    "tip": "Use lukewarm water and pat dry gently"
                },
                {
                    "step_number": "2",
                    "name": f"Apply {product_name} - First Application",
                    "description": f"Apply {product_name} to entire face. {description}",
                    "tip": "Use the recommended amount from the product label",
                    "product_focus": product
                },
                {
                    "step_number": "3",
                    "name": f"Let it Absorb",
                    "description": f"Allow {product_name} to absorb for 1-2 minutes before next step",
                    "tip": "Don't rush - better absorption means better results"
                },
                {
                    "step_number": "4",
                    "name": f"Layer with Complementary Product",
                    "description": f"Once {product_name} absorbs, apply light moisturizer or sunscreen",
                    "tip": "This helps lock in the benefits"
                },
                {
                    "step_number": "5",
                    "name": f"Sunscreen",
                    "description": "Always apply SPF 30+ sunscreen as final step",
                    "tip": "Essential for protecting skin and preventing further damage"
                }
            ]
        },
        "evening": {
            "steps": [
                {
                    "step_number": "1",
                    "name": f"Gentle Cleanse",
                    "description": f"Remove makeup and impurities with a gentle cleanser",
                    "tip": "Prepare skin to receive {product_name} benefits"
                },
                {
                    "step_number": "2",
                    "name": f"Apply {product_name} - Primary Application",
                    "description": f"Apply {product_name} generously to face. {description}",
                    "tip": "Evening is when skin repairs, so product absorption is optimal",
                    "product_focus": product
                },
                {
                    "step_number": "3",
                    "name": f"Boost with Additional Product",
                    "description": f"For concentrated effect, apply thin extra layer of {product_name}",
                    "tip": "Optional but recommended for intensive treatment"
                },
                {
                    "step_number": "4",
                    "name": f"Layer Moisturizer",
                    "description": f"Apply rich night moisturizer to seal in {product_name}",
                    "tip": "Creates occlusive layer for maximum hydration"
                },
                {
                    "step_number": "5",
                    "name": f"Spot Treatment (if applicable)",
                    "description": f"If targeting specific concern ({concern}), apply {product_name} to affected areas",
                    "tip": "Allows product to work intensively on problem areas overnight",
                    "product_focus": product
                }
            ]
        }
    }
    
    return routine