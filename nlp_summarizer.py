def simple_summarize(note_text: str, max_sentences: int = 3) -> str:
    """
    A simple summarizer that extracts the most important sentences
    (without requiring spaCy which can be heavy for Streamlit sharing).

    Args:
        note_text: Full text of the doctor's notes.
        max_sentences: Maximum number of sentences to include in summary.

    Returns:
        A concise summary.
    """
    if not note_text:
        return "No text provided."
    
    # Split by periods to get sentences
    sentences = [s.strip() for s in note_text.split('.') if s.strip()]
    
    # For simplicity, return the first few sentences
    summary_sentences = sentences[:max_sentences]
    
    # Join with periods
    summary = '. '.join(summary_sentences)
    if summary and not summary.endswith('.'):
        summary += '.'
        
    return summary

def extract_key_info(note_text: str) -> dict:
    """
    Extract key medical information from doctor notes.
    
    This is a simulation - in a real application, use a proper NLP model.
    
    Args:
        note_text: Doctor's notes text.
        
    Returns:
        Dictionary of key information.
    """
    # Keywords to look for (simulating NLP entity extraction)
    keywords = {
        "diagnosis": ["diagnosed with", "diagnosis", "condition"],
        "medication": ["prescribed", "medication", "take", "mg", "dose"],
        "follow_up": ["follow up", "weeks", "appointment", "visit"]
    }
    
    results = {
        "diagnosis": [],
        "medication": [],
        "follow_up": []
    }
    
    # Split text into sentences
    sentences = [s.strip() for s in note_text.split('.') if s.strip()]
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        # Check for keyword matches
        for category, terms in keywords.items():
            if any(term in sentence_lower for term in terms):
                results[category].append(sentence)
    
    return results 