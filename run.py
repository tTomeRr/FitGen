"""
This module sets up and runs the flex Flask web application.
it runs the app on host 0.0.0.0 and port 5000.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
