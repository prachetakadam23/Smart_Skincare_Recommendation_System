"""
NLP Model for Skincare Chatbot
Uses pattern matching and rule-based approach for intelligent skincare responses
"""

import re
from typing import Dict, List, Tuple

# Skincare knowledge base
SKINCARE_KNOWLEDGE = {
    "acne": {
        "causes": ["excess oil", "bacteria", "clogged pores", "hormonal changes"],
        "remedies": ["salicylic acid", "benzoyl peroxide", "retinoids", "azelaic acid"],
        "products": ["acne cleanser", "acne serum", "acne spot treatment"],
        "tips": ["avoid touching face", "use oil-free products", "change pillowcase regularly", "reduce dairy intake"]
    },
    "dryness": {
        "causes": ["dehydration", "harsh weather", "over-cleansing", "genetic factors"],
        "remedies": ["hyaluronic acid", "glycerin", "ceramides", "niacinamide"],
        "products": ["hydrating cleanser", "hydrating serum", "rich moisturizer"],
        "tips": ["use lukewarm water", "apply moisturizer to damp skin", "use humidifier", "avoid hot showers"]
    },
    "oiliness": {
        "causes": ["sebum production", "hormones", "humidity", "diet"],
        "remedies": ["niacinamide", "salicylic acid", "zinc", "clay masks"],
        "products": ["oil-free cleanser", "mattifying serum", "oil-free moisturizer"],
        "tips": ["use blotting papers", "avoid heavy moisturizers", "cleanse twice daily", "use oil-free sunscreen"]
    },
    "wrinkles": {
        "causes": ["aging", "sun damage", "smoking", "dehydration"],
        "remedies": ["retinol", "vitamin C", "peptides", "hyaluronic acid"],
        "products": ["anti-aging serum", "retinol cream", "eye cream"],
        "tips": ["use sunscreen daily", "moisturize regularly", "sleep 8 hours", "stay hydrated"]
    },
    "dark_spots": {
        "causes": ["sun damage", "aging", "hormones", "inflammation"],
        "remedies": ["vitamin C", "niacinamide", "kojic acid", "hydroquinone"],
        "products": ["brightening serum", "dark spot treatment", "sunscreen"],
        "tips": ["wear sunscreen SPF 50+", "use daily", "take breaks in sun", "avoid picking skin"]
    },
    "pigmentation": {
        "causes": ["sun exposure", "genetics", "hormones", "inflammation"],
        "remedies": ["vitamin C", "kojic acid", "licorice extract", "sunscreen"],
        "products": ["brightening serum", "pigmentation treatment"],
        "tips": ["use SPF 50+ daily", "reapply sunscreen every 2 hours", "avoid sun 10am-4pm"]
    },
    "pores": {
        "causes": ["genetics", "large sebaceous glands", "lack of hydration", "sun damage"],
        "remedies": ["retinol", "niacinamide", "salicylic acid", "hydration"],
        "products": ["pore-minimizing serum", "clay mask", "mild cleanser"],
        "tips": ["regular exfoliation", "stay hydrated", "use pore mask weekly", "keep skin moisturized"]
    },
    "blackheads": {
        "causes": ["clogged pores", "excess oil", "bacteria", "dead skin cells"],
        "remedies": ["salicylic acid", "benzoyl peroxide", "retinoids", "charcoal"],
        "products": ["blackhead treatment", "exfoliating cleanser", "pore strips"],
        "tips": ["exfoliate 2-3 times weekly", "don't squeeze", "use salicylic acid serum", "steam face"]
    }
}

# Intent patterns
INTENT_PATTERNS = {
    "concern_inquiry": [
        r".*\b(what|how|why|tell|explain).*(\bacne\b|\bdryness\b|\boiliness\b|\bwrinkles\b|\bdark.?spots?\b|\bpigmentation\b|\bpores?\b|\bblackheads?\b)",
        r".*\b(acne|dryness|oiliness|wrinkles|dark.?spots?|pigmentation|pores?|blackheads?).*\b(problem|issue|concern|cause|reason)",
        r".*i have.*(acne|dryness|oiliness|wrinkles|dark.?spots?|pigmentation|large pores|blackheads)",
    ],
    "remedy_inquiry": [
        r".*\b(what|how|best|recommend).*\b(for|treat|cure|fix|solve).*",
        r".*\bhow.*(acne|dryness|oiliness|wrinkles|dark.?spots?|pigmentation|pores?|blackheads)",
        r".*\b(treatment|remedy|solution|cure).*(acne|dryness|oiliness|wrinkles|dark.?spots?|pigmentation|pores?|blackheads)",
    ],
    "product_inquiry": [
        r".*\b(what|best|recommend).*\b(product|serum|cream|moisturizer|cleanser|sunscreen)",
        r".*\b(product|serum|cream|moisturizer|cleanser|sunscreen|ingredient).*\b(for|recommend|suggest)",
    ],
    "routine_inquiry": [
        r".*\b(routine|steps?|how|way|process).*\b(skin|care|morning|evening|daily)",
        r".*\b(morning|evening|daily).*(routine|skincare|steps?)",
    ],
    "ingredient_inquiry": [
        r".*\b(ingredient|ingredient|chemical|component).*",
        r".*\b(what|contain|ingredients?|contain).*",
    ],
    "tip_inquiry": [
        r".*\b(tip|trick|advice|suggestion|help).*",
        r".*\b(help|how|can|should|must).*(do|use|apply)",
    ],
    "greeting": [
        r"^(hello|hi|hey|greetings?)$",
        r"^(how are you|what's up|good morning|good evening).*",
    ],
    "gratitude": [
        r"^(thank|thanks|thankyou|appreciate).*",
        r"^(great|awesome|perfect|thanks).*",
    ],
}

# Responses
RESPONSES = {
    "greeting": [
        "Hello! 👋 I'm Skinify, your skincare assistant. How can I help you today?",
        "Hi there! 😊 I'm here to help with your skincare concerns. What's on your mind?",
        "Hello! 🌟 Ready to learn more about skincare? Ask me anything!",
    ],
    "gratitude": [
        "Happy to help! Feel free to ask if you need more advice. 💫",
        "You're welcome! Keep taking care of your skin! 💗",
        "My pleasure! Good luck with your skincare journey! ✨",
    ],
    "concern_explanation": [
        "I understand you're interested in {concern}. Let me help! This typically happens due to {cause}. I recommend {remedy}. Use products with {product} regularly. 💡",
        "{concern.capitalize()} is a common concern caused by {cause}. The best approach is to use {remedy} consistently. Recommended products include {product}. 🌿",
    ],
    "remedy_suggestion": [
        "For {concern}, I highly recommend trying {remedy}. Apply once daily for best results. Be patient - skin usually shows improvement in 4-8 weeks! ⏰",
        "The most effective remedy for {concern} is {remedy}. Use it as part of your daily routine, especially in the evening. You should see results in about a month! 🎯",
    ],
    "product_recommendation": [
        "For your concerns, I recommend: {products}. Use these consistently as part of your skincare routine. Quality matters! 💯",
        "Great products to address your needs: {products}. Start with one and see how your skin reacts before adding more. 🧴",
    ],
    "routine_suggestion": [
        "A good skincare routine has 5 steps: 1) Cleanse 2) Tone 3) Apply Serum 4) Moisturize 5) Sunscreen. Morning and evening routines should be similar, but evening can include stronger treatments. 🌙",
        "Follow this routine: Morning - Cleanser → Toner → Serum → Moisturizer → SPF 50. Evening - Cleanser → Toner → Treatment → Moisturizer. Consistency is key! ✨",
    ],
    "tip_suggestion": [
        "{tip}. This small habit can make a big difference in your skin health! 🌟",
        "Here's a helpful tip: {tip}. Try incorporating this into your routine! 💪",
    ],
    "default": [
        "That's an interesting question! Could you tell me more about your skin concerns or what you'd like to know about skincare? 🤔",
        "I'm here to help with skincare advice. What specific concern would you like to address? 💭",
    ],
}


class SkincareNLPChatbot:
    """Intelligent chatbot for skincare advice"""
    
    def __init__(self):
        self.knowledge = SKINCARE_KNOWLEDGE
        self.patterns = INTENT_PATTERNS
        self.responses = RESPONSES
    
    def extract_concern(self, text: str) -> str:
        """Extract skincare concern from text"""
        text_lower = text.lower()
        for concern in self.knowledge.keys():
            pattern = concern.replace("_", ".?")
            if re.search(pattern, text_lower):
                return concern
        return None
    
    def detect_intent(self, text: str) -> str:
        """Detect user intent from message"""
        text_lower = text.lower().strip()
        
        # Check each intent pattern
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return intent
        
        return "default"
    
    def get_random_from_list(self, items: List[str]) -> str:
        """Get a random item from list (or first if list)"""
        return items[0] if items else ""
    
    def generate_response(self, user_message: str) -> str:
        """Generate response based on user message"""
        intent = self.detect_intent(user_message)
        concern = self.extract_concern(user_message)
        
        if intent == "greeting":
            return self.get_random_from_list(self.responses["greeting"])
        
        elif intent == "gratitude":
            return self.get_random_from_list(self.responses["gratitude"])
        
        elif intent == "concern_inquiry" and concern:
            knowledge = self.knowledge[concern]
            response = self.get_random_from_list(self.responses["concern_explanation"])
            cause = self.get_random_from_list(knowledge["causes"])
            remedy = self.get_random_from_list(knowledge["remedies"])
            product = self.get_random_from_list(knowledge["products"])
            return response.format(concern=concern, cause=cause, remedy=remedy, product=product)
        
        elif intent == "remedy_inquiry" and concern:
            knowledge = self.knowledge[concern]
            response = self.get_random_from_list(self.responses["remedy_suggestion"])
            remedy = self.get_random_from_list(knowledge["remedies"])
            return response.format(concern=concern, remedy=remedy)
        
        elif intent == "product_inquiry":
            if concern:
                knowledge = self.knowledge[concern]
                products = ", ".join(knowledge["products"][:2])
            else:
                products = "cleanser, serum, and moisturizer"
            response = self.get_random_from_list(self.responses["product_recommendation"])
            return response.format(products=products)
        
        elif intent == "routine_inquiry":
            return self.get_random_from_list(self.responses["routine_suggestion"])
        
        elif intent == "tip_inquiry" and concern:
            knowledge = self.knowledge[concern]
            tip = self.get_random_from_list(knowledge["tips"])
            response = self.get_random_from_list(self.responses["tip_suggestion"])
            return response.format(tip=tip)
        
        else:
            return self.get_random_from_list(self.responses["default"])
    
    def chat(self, user_message: str) -> Dict:
        """Process user message and return response"""
        response_text = self.generate_response(user_message)
        intent = self.detect_intent(user_message)
        concern = self.extract_concern(user_message)
        
        return {
            "reply": response_text,
            "intent": intent,
            "concern": concern
        }


# Initialize chatbot
chatbot = SkincareNLPChatbot()


def get_chat_response(message: str) -> str:
    """Public function to get chat response"""
    result = chatbot.chat(message)
    return result["reply"]
