import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to run your code and capture output
def run_script():
    # Replace 'your_script.py' with the path to your script
    result = subprocess.run(['python3', '/home/kali/Desktop/Kite_Zerodha-main/codebase/chartink_main.py'], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr

# Email details
sender_email = "snehalsanketgunge@gmail.com"   # Replace with your email
receiver_email = "snehalsanketgunge@gmail.com"  # Replace with receiver's email
password = "fdya eaus zxcn urnl"  # Replace with your email password

# Compose the email
def send_email(script_output):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Python Script Output"

    # Attach the script output
    msg.attach(MIMEText(script_output, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

# Run the script and send the output
output = run_script()
send_email(output)

