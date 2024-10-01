from app import create_app

app = create_app()

if __name__ == "__main__":
    # Bind to all network interfaces (0.0.0.0) and run on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
