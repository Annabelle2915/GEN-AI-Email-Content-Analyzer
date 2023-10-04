# Import necessary libraries
import streamlit as st  # Import the Streamlit library and alias it as 'st'
import email_analyzer  # Import your custom module for email analysis

# Set the page layout to be wide
st.set_page_config(layout="wide")  # 'st.set_page_config' is a method to configure the layout of the web page

# Display the title and usage instructions
st.title("✉️ Email Content Analyzer")  # 'st.title' is a method to display a title on the web page
st.write(
        "Welcome to Email Content Analyzer! This web app helps you classify, extract, and summarize email content. ",
        "To get started, enter the email subject, sender's name, sender's email, and paste the email content in the respective fields. ",
        "Click the 'Classify, Extract, and Summarize' button to see the analysis results in the sidebar.",

        )   # 'st.write' is a method to display text or other content on the web page
     # Set the font size to be smaller


# Add a space (empty string) between the title and user inputs
st.text("")  # or st.write("")

# User inputs for email subject, sender name, and sender email
email_subject = st.text_input("Email Subject:")  # 'st.text_input' is a method to create a text input field
sender_name = st.text_input("Sender's Name:")  # 'st.text_input' for another text input field
sender_email = st.text_input("Sender's Email:")  # 'st.text_input' for another text input field

# Email content input
email_text = st.text_area("Paste your email content here:", height=400, max_chars=5000)  # 'st.text_area' creates a multiline text input field

# Create columns for button and result display
button_col, result_col = st.columns([1, 1])  # 'st.columns' is a method to create columns for layout

# Inside the button column, check if the "Classify, Extract, and Summarize" button is clicked
with button_col:
    if st.button("Classify, Extract, and Summarize", key="classify_button"):
        # Check if all required fields are filled out
        if email_subject and sender_name and sender_email and email_text:
            try:
                # Call the function from the custom module to classify, summarize, and analyze sentiment of the email
                classification_result, sentiment_score, sentiment_label, summarized_text = email_analyzer.classify_and_summarize_email(
                    email_subject, sender_name, sender_email, email_text
                )
                # Update the sidebar with classification, sentiment, and summary results
                # Classification and Sender Information Section
                st.sidebar.markdown("<h2 style='font-size: 1.5em;'>Classification & Sender Information</h2>", unsafe_allow_html=True)
                 # Display the clean classification result
                st.sidebar.markdown(f"<b>Category:</b> {classification_result}", unsafe_allow_html=True)                
                st.sidebar.markdown(f"<b>Sentiment:</b> {sentiment_label}", unsafe_allow_html=True)
                st.sidebar.markdown(f"<b>Email Subject:</b> {email_subject}", unsafe_allow_html=True)
                st.sidebar.markdown(f"<b>Sender:</b> {sender_name} &lt;{sender_email}&gt;", unsafe_allow_html=True)

                # Divider Line
                st.sidebar.markdown("<hr style='margin-top: 20px;'>", unsafe_allow_html=True)

                # Summarized Email Section
                st.sidebar.markdown("<h2>Summarized Email</h2>", unsafe_allow_html=True)
                st.sidebar.markdown(summarized_text)

                # Divider Line
                st.sidebar.markdown("<hr style='margin-top: 20px;'>", unsafe_allow_html=True)
                
                with st.sidebar.expander("Sentiment Explanation"):
                    st.markdown("The sentiment of the email is determined based on its content. Here's what each label means:")
                    st.markdown("- **Positive 😊:** The email has a positive tone.")
                    st.markdown("- **Negative 😞:** The email has a negative tone.")
                    st.markdown("- **Neutral 😐:** The email doesn't exhibit strong positive or negative sentiment.")
                


               






            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill out all fields before classifying, extracting, and summarizing.")



