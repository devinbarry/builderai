from flask import request, jsonify
from .models import db, Trade


def register_routes(app):
    @app.route('/trades', methods=['POST'])
    def create_trade():
        try:
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400

            data = request.get_json()

            required_fields = ['type', 'user_id', 'symbol', 'shares', 'price', 'timestamp']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400

            if not isinstance(data['user_id'], int):
                return jsonify({'error': 'user_id must be an integer'}), 400
            if not isinstance(data['shares'], int):
                return jsonify({'error': 'shares must be an integer'}), 400
            if not isinstance(data['price'], int):
                return jsonify({'error': 'price must be an integer'}), 400
            if not isinstance(data['type'], str):
                return jsonify({'error': 'type must be a string'}), 400
            if not isinstance(data['symbol'], str):
                return jsonify({'error': 'symbol must be a string'}), 400

            new_trade = Trade(
                type=data['type'],
                user_id=data['user_id'],
                symbol=data['symbol'],
                shares=data['shares'],
                price=data['price'],
                timestamp=data['timestamp']
            )

            db.session.add(new_trade)
            db.session.commit()

            return jsonify({
                'id': new_trade.id,
                'type': new_trade.type,
                'user_id': new_trade.user_id,
                'symbol': new_trade.symbol,
                'shares': new_trade.shares,
                'price': new_trade.price,
                'timestamp': new_trade.timestamp
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/trades', methods=['GET'])
    def get_trades():
        trades = Trade.query.order_by(Trade.id).all()
        return jsonify([{
            'id': trade.id,
            'type': trade.type,
            'user_id': trade.user_id,
            'symbol': trade.symbol,
            'shares': trade.shares,
            'price': trade.price,
            'timestamp': trade.timestamp
        } for trade in trades]), 200

    @app.route('/trades/<int:trade_id>', methods=['GET'])
    def get_trade(trade_id):
        trade = db.session.get(Trade, trade_id)
        if trade is None:
            return '', 404

        return jsonify({
            'id': trade.id,
            'type': trade.type,
            'user_id': trade.user_id,
            'symbol': trade.symbol,
            'shares': trade.shares,
            'price': trade.price,
            'timestamp': trade.timestamp
        }), 200

    # Handle methods that should return 405
    @app.route('/trades/<int:trade_id>', methods=['PUT', 'PATCH', 'DELETE'])
    def method_not_allowed(trade_id):
        return '', 405