import imaplib
import email
from email.header import decode_header
import time

username = "codeinrishabh@gmail.com"
password = "dehm xbyw cxsr ktlv"
imap_server = "imap.gmail.com"  # Using Gmail's IMAP server

# Target sender email address
target_sender = "action@ifttt.com"

# Maximum number of connection attempts
MAX_RETRIES = 3

# Establish IMAP connection with retries
for attempt in range(MAX_RETRIES):
    try:
        print(f"Connecting to IMAP server... Attempt {attempt+1}/{MAX_RETRIES}")
        # Create a new connection on each attempt with a timeout
        mail = imaplib.IMAP4_SSL(imap_server, timeout=10)
        try:
            # Attempt login (if already authenticated, skip login)
            mail.login(username, password)
        except imaplib.IMAP4.error as e:
            if "illegal in state AUTH" in str(e):
                print("Already logged in, skipping login.")
            else:
                raise
        print("Successfully connected to IMAP server!")
        break  # Exit loop on success
    except Exception as e:
        print(f"Error connecting to IMAP server: {e}")
        try:
            mail.logout()
        except Exception:
            pass
        time.sleep(3)
else:
    print("Failed to connect to IMAP server after multiple attempts. Exiting.")
    exit()

# Select the "inbox" mailbox
try:
    status, _ = mail.select("inbox")
    if status != "OK":
        print("Failed to select inbox")
        mail.logout()
        exit()
except Exception as e:
    print(f"Error selecting inbox: {e}")
    mail.logout()
    exit()

# Search for emails from the specified target sender
status, message_numbers = mail.search(None, f'FROM "{target_sender}"')
if status != "OK":
    print("Error searching for emails.")
    mail.logout()
    exit()

email_ids = message_numbers[0].split()

if not email_ids:
    print("No emails found from the specified sender.")
else:
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            print(f"Failed to fetch email ID: {email_id}")
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Decode the email subject for reference
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        print(f"Processing email: {subject}")

        # Extract the email body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                # Look for plain text parts that are not attachments
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        charset = part.get_content_charset() or "utf-8"
                        body = part.get_payload(decode=True).decode(charset, errors="ignore")
                    except Exception as e:
                        print(f"Error decoding email body: {e}")
                    break  # Stop after finding the plain text part
        else:
            try:
                body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")
            except Exception as e:
                print(f"Error decoding email body: {e}")

        # Save the email subject and body to a text file if available
        if body.strip():
            with open("email_body.txt", "a", encoding="utf-8") as file:
                file.write(body)
                file.write("\n" + "=" * 50 + "\n")  # Separator between emails
        else:
            print(f"Warning: No text content found in email ID {email_id}")

    print("Email bodies saved to 'email_body.txt'.")

# Attempt to close the mailbox if selected, otherwise skip
try:
    mail.close()
except imaplib.IMAP4.error:
    print("No mailbox selected, skipping close()")

# Logout to cleanly close the connection
mail.logout()