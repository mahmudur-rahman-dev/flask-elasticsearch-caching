from src.routes import createApp
app = createApp()
# redis_client.publish('asdfsd', "ok");
if __name__ == "__main__":
    app.run()