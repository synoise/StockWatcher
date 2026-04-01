from flask import Flask

app = Flask(__name__)

# Import routes
from routes.stock_data import stock_data_bp
from routes.predictions import predictions_bp
from routes.portfolio import portfolio_bp
from websocket.websocket import websocket_bp

# Register blueprints
app.register_blueprint(stock_data_bp)
app.register_blueprint(predictions_bp)
app.register_blueprint(portfolio_bp)
app.register_blueprint(websocket_bp)

if __name__ == '__main__':
    app.run(debug=True)