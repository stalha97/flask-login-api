from myApi import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="192.168.100.214")