"""Main Flask application for Campus Parking System"""
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ParkingLot, ParkingSpace, User, Reservation
from parking_lot import ParkingLotClass, ParkingSpaceClass
import os

app = Flask(__name__)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///parking.db')
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route('/api/lots', methods=['GET'])
def get_lots():
    """Get all parking lots"""
    session = Session()
    lots = session.query(ParkingLot).all()
    data = [{
        'lot_id': lot.lot_id,
        'name': lot.name,
        'location': lot.location,
        'total_spaces': lot.total_spaces,
        'available_spaces': lot.available_spaces,
        'occupancy_rate': lot.occupancy_rate
    } for lot in lots]
    session.close()
    return jsonify(data)


@app.route('/api/lots/<int:lot_id>/spaces', methods=['GET'])
def get_lot_spaces(lot_id):
    """Get all spaces in a parking lot"""
    session = Session()
    lot = session.query(ParkingLot).filter_by(lot_id=lot_id).first()
    if not lot:
        session.close()
        return jsonify({'error': 'Lot not found'}), 404
    
    spaces = [{
        'space_id': space.space_id,
        'space_number': space.space_number,
        'category': space.category,
        'is_available': space.is_available
    } for space in lot.spaces]
    session.close()
    return jsonify(spaces)


@app.route('/api/spaces/available', methods=['GET'])
def get_available_spaces():
    """Get all available spaces"""
    session = Session()
    category = request.args.get('category')
    query = session.query(ParkingSpace).filter_by(is_available=True)
    if category:
        query = query.filter_by(category=category)
    spaces = query.all()
    data = [{
        'space_id': space.space_id,
        'space_number': space.space_number,
        'lot_id': space.lot_id,
        'category': space.category
    } for space in spaces]
    session.close()
    return jsonify(data)


@app.route('/api/status', methods=['GET'])
def system_status():
    """Get system status"""
    session = Session()
    total_lots = session.query(ParkingLot).count()
    total_spaces = session.query(ParkingSpace).count()
    available_spaces = session.query(ParkingSpace).filter_by(is_available=True).count()
    session.close()
    
    return jsonify({
        'total_lots': total_lots,
        'total_spaces': total_spaces,
        'available_spaces': available_spaces,
        'occupancy_rate': round((total_spaces - available_spaces) / total_spaces * 100, 2) if total_spaces > 0 else 0
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
