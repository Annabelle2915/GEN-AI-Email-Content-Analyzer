import openai
import re
from textblob import TextBlob

# Set your OpenAI API key
api_key = ""
openai.api_key = api_key

def extract_subject_and_sender(email_text):
    # Regular expression pattern for matching subject and sender lines
    subject_pattern = re.compile(r'^Subject:(.*$)|^Subject\s*[:-](.*$)', re.I)
    from_pattern = re.compile(r'^From:(.*$)|^From\s*[:-](.*$)', re.I)
    
    subject = "No Subject"
    sender = "Unknown Sender"
    
    # Split the email content into lines
    lines = email_text.split("\n")
    
    for line in lines:
        # Try to match the subject line using the pattern
        subject_match = subject_pattern.match(line)
        if subject_match:
            subject = subject_match.group(1) or subject_match.group(2)
            subject = subject.strip()

        # Try to match the sender line using the pattern
        sender_match = from_pattern.match(line)
        if sender_match:
            sender = sender_match.group(1) or sender_match.group(2)
            sender = sender.strip()

    return subject, sender

def classify_and_summarize_email(email_subject, sender_name, sender_email, email_text):
    try:
        # Request problem category classification using OpenAI API
        response_classification = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Classify the content of email into its related field:\n{email_text}",
            max_tokens=10,  # Set maximum tokens for the response, adjust as needed
            n=1
        )
        classification_result = response_classification.choices[0].text.strip().rstrip('.')

        # Extract email subject and sender using a helper function
        subject, sender = extract_subject_and_sender(email_text)
        
        # Perform sentiment analysis using TextBlob
        sentiment = TextBlob(email_text).sentiment
        sentiment_score = sentiment.polarity  # Sentiment score ranging from -1 to 1
        
        # Determine sentiment label
        if sentiment_score > 0.1:
            sentiment_label = "Positive 😊"
        elif sentiment_score < -0.1:
            sentiment_label = "Negative 😞"
        else:
            sentiment_label = "Neutral 😐"
        
        # Request email summarization using OpenAI API
        response_summarization = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following email content:\n{email_text}",
            max_tokens=150,  # Set maximum tokens for the summary, adjust as needed
            n=1
        )
        summarized_text = response_summarization.choices[0].text.strip()

        # Return the classification result, sentiment score, sentiment label, and summarized text
        return classification_result, sentiment_score, sentiment_label, summarized_text

    except Exception as e:
        # Handle any exceptions that occur during the classification or summarization process
        raise Exception(f"An error occurred: {e}")
