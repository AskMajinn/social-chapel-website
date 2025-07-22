#!/usr/bin/env python3
"""
Simple HTTP server to handle Google Forms iframe redirect issue
This server acts as a proxy to capture form submissions and redirect properly
"""

import http.server
import socketserver
import urllib.parse
import urllib.request
import json
from urllib.parse import urlparse, parse_qs

class FormProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_url = urlparse(self.path)
        
        # If it's a request for our form proxy
        if parsed_url.path == '/form-proxy':
            self.handle_form_proxy()
        # If it's a request for the thank you redirect
        elif parsed_url.path == '/form-redirect':
            self.handle_form_redirect()
        else:
            # Serve static files normally
            super().do_GET()
    
    def do_POST(self):
        # Handle form submissions
        if self.path == '/form-submit':
            self.handle_form_submission()
        else:
            super().do_POST()
    
    def handle_form_proxy(self):
        """Serve a modified form that submits to our server"""
        form_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wedding Form</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .form-container { max-width: 600px; margin: 0 auto; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
                button { background: #d4af37; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
                button:hover { background: #b8941f; }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h2>Wedding & Quinceañera Inquiry Form</h2>
                <form action="/form-submit" method="post">
                    <div class="form-group">
                        <label for="name">Full Name *</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email Address *</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone Number *</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="event_date">Event Date</label>
                        <input type="date" id="event_date" name="event_date">
                    </div>
                    
                    <div class="form-group">
                        <label for="event_type">Event Type</label>
                        <select id="event_type" name="event_type">
                            <option value="">Select an option</option>
                            <option value="wedding">Wedding</option>
                            <option value="quinceanera">Quinceañera</option>
                            <option value="both">Both Wedding & Quinceañera</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="guest_count">Expected Number of Guests</label>
                        <input type="number" id="guest_count" name="guest_count" min="1">
                    </div>
                    
                    <div class="form-group">
                        <label for="message">Additional Information</label>
                        <textarea id="message" name="message" rows="4" placeholder="Tell us more about your event..."></textarea>
                    </div>
                    
                    <button type="submit">Submit Inquiry</button>
                </form>
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(form_html.encode())
    
    def handle_form_submission(self):
        """Handle the form submission and redirect"""
        try:
            # Get the form data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)
            
            # Log the submission (you could save to database here)
            print("Form submission received:")
            for key, value in form_data.items():
                print(f"  {key}: {value[0] if value else ''}")
            
            # Redirect to thank you page
            self.send_response(302)
            self.send_header('Location', '/sc-thankyou.html')
            self.end_headers()
            
        except Exception as e:
            print(f"Error handling form submission: {e}")
            self.send_response(500)
            self.end_headers()
    
    def handle_form_redirect(self):
        """Handle redirect from Google Forms"""
        # Parse query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Redirect to thank you page
        self.send_response(302)
        self.send_header('Location', '/sc-thankyou.html')
        self.end_headers()

def run_server(port=3001):
    """Start the proxy server"""
    try:
        with socketserver.TCPServer(("", port), FormProxyHandler) as httpd:
            print(f"Form proxy server running on http://localhost:{port}")
            print(f"Form URL: http://localhost:{port}/form-proxy")
            print(f"Static files served from current directory")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    run_server()
