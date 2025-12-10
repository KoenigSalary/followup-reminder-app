"""
ROBUST JSON PARSER for AI MoM Extractor
Handles all markdown fence variations that OpenAI might return
"""

import json
import re

def clean_and_parse_json(ai_response):
    """
    Robustly clean and parse JSON from AI response.
    Handles markdown fences, extra whitespace, and other common issues.
    """
    
    # Step 1: Strip outer whitespace
    cleaned = ai_response.strip()
    
    # Step 2: Remove markdown code fences
    # Pattern 1: ```json ... ```
    if cleaned.startswith('```json'):
        cleaned = cleaned[7:]  # Remove ```json
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]  # Remove trailing ```
    
    # Pattern 2: ``` ... ```
    elif cleaned.startswith('```'):
        cleaned = cleaned[3:]  # Remove ```
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]  # Remove trailing ```
    
    # Step 3: Strip again after removing fences
    cleaned = cleaned.strip()
    
    # Step 4: Try to find JSON array/object if there's extra text
    # Look for [ ... ] or { ... }
    json_match = re.search(r'(\[.*\]|\{.*\})', cleaned, re.DOTALL)
    if json_match:
        cleaned = json_match.group(1)
    
    # Step 5: Parse JSON
    try:
        parsed = json.loads(cleaned)
        return parsed, None  # Success, no error
    except json.JSONDecodeError as e:
        return None, str(e)  # Failed, return error


# TEST CASES
if __name__ == "__main__":
    print("=" * 70)
    print("🧪 TESTING ROBUST JSON PARSER")
    print("=" * 70)
    
    test_cases = [
        # Case 1: Clean JSON
        '''[{"title": "Task 1", "deadline": "2025-12-15"}]''',
        
        # Case 2: With ```json fence
        '''```json
[{"title": "Task 1", "deadline": "2025-12-15"}]
```''',
        
        # Case 3: With ``` fence (no language)
        '''```
[{"title": "Task 1", "deadline": "2025-12-15"}]
```''',
        
        # Case 4: With extra text before
        '''Here are the tasks:
[{"title": "Task 1", "deadline": "2025-12-15"}]''',
        
        # Case 5: With extra whitespace
        '''
        
        [{"title": "Task 1", "deadline": "2025-12-15"}]
        
        ''',
        
        # Case 6: Invalid JSON (should fail gracefully)
        '''This is not JSON at all'''
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Input (first 60 chars): {repr(test[:60])}...")
        
        result, error = clean_and_parse_json(test)
        
        if result:
            print(f"✅ SUCCESS: Parsed {len(result)} items")
        else:
            print(f"❌ FAILED: {error}")
    
    print("\n" + "=" * 70)
