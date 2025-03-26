from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static', template_folder='templates')

# Data storage for recommendations
TRIP_DATA = {
    'packing': {
        'Goa': 'Light clothes, sunscreen, sunglasses, swimwear',
        'Manali': 'Warm clothes, jackets, gloves, thermals',
        'Mumbai': 'Umbrella, light clothes, raincoat',
        'Delhi': 'Comfortable clothes, sunscreen, scarf',
        'Bangalore': 'Light jacket, comfortable shoes, umbrella'
    },
    'transport': {
        'bus': ['RedBus: 10:00 AM', 'VRL: 2:00 PM', 'KSRTC: 6:00 PM'],
        'train': ['Rajdhani: 9:00 AM', 'Shatabdi: 5:00 PM', 'Duronto: 11:00 PM'],
        'flight': ['Indigo: 8:00 AM', 'Air India: 6:00 PM', 'Vistara: 3:00 PM']
    },
    'stay': {
        'budget': ['OYO Rooms', 'FabHotels', 'Zostel', 'Treebo'],
        'premium': ['Taj Hotels', 'Leela Palace', 'Oberoi', 'ITC Hotels'],
        'business': ['Marriott', 'Hyatt', 'Hilton', 'Radisson']
    },
    'food': {
        'indian': ['Biryani House', 'Rajdhani Thali', 'Saravana Bhavan'],
        'chinese': ['Mainland China', 'Beijing Bites', 'Nanking'],
        'local': ['Goan Seafood', 'Mumbai Vada Pav', 'Delhi Chaat']
    },
    'places': {
        'beaches': ['Baga Beach', 'Palolem Beach', 'Marina Beach'],
        'pilgrims': ['Tirupati Temple', 'Golden Temple', 'Meenakshi Temple'],
        'local': ['Gateway of India', 'Marine Drive', 'India Gate']
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trip_form', methods=['POST'])
def trip_form():
    trip_type = request.form['trip_type']
    return render_template('trip_form.html', trip_type=trip_type)

@app.route('/smart_packaging', methods=['POST'])
def smart_packaging():
    trip_type = request.form['trip_type']
    start_place = request.form['start_place']
    destination = request.form['destination']
    travel_dates = request.form['travel_dates']
    
    # Add business-specific packing items
    packing_list = TRIP_DATA['packing'].get(destination, 'Casual clothes')
    if trip_type == 'business':
        packing_list = 'Business attire, laptop, documents | ' + packing_list
    
    return render_template('smart_packaging.html',
                         trip_type=trip_type,
                         start_place=start_place,
                         destination=destination,
                         travel_dates=travel_dates,
                         packing_list=packing_list)

@app.route('/transport_options', methods=['POST'])
def transport_options():
    trip_data = {
        'trip_type': request.form['trip_type'],
        'start_place': request.form['start_place'],
        'destination': request.form['destination'],
        'travel_dates': request.form['travel_dates']
    }
    
    transport_mode = request.form.get('transport_mode')
    if transport_mode:
        options = TRIP_DATA['transport'].get(transport_mode, [])
        return render_template('transport_display.html',
                            transport_mode=transport_mode,
                            options=options,
                            **trip_data)
    
    return render_template('transport_options.html', **trip_data)

@app.route('/stay_options', methods=['POST'])
def stay_options():
    trip_data = {
        'trip_type': request.form['trip_type'],
        'start_place': request.form['start_place'],
        'destination': request.form['destination'],
        'travel_dates': request.form['travel_dates'],
        'transport_mode': request.form['transport_mode']
    }
    
    stay_type = request.form.get('stay_type')
    if stay_type:
        options = TRIP_DATA['stay'].get(stay_type, [])
        # Business trips get business stays by default
        if trip_data['trip_type'] == 'business' and stay_type != 'business':
            options = TRIP_DATA['stay']['business']
        
        return render_template('stay_display.html',
                            stay_type=stay_type,
                            options=options,
                            **trip_data)
    
    return render_template('stay_options.html', **trip_data)

@app.route('/food_options', methods=['POST'])
def food_options():
    trip_data = {
        'trip_type': request.form['trip_type'],
        'start_place': request.form['start_place'],
        'destination': request.form['destination'],
        'travel_dates': request.form['travel_dates'],
        'transport_mode': request.form['transport_mode'],
        'stay_type': request.form['stay_type']
    }
    
    food_type = request.form.get('food_type')
    if food_type:
        options = TRIP_DATA['food'].get(food_type, [])
        return render_template('food_display.html',
                            food_type=food_type,
                            options=options,
                            **trip_data)
    
    return render_template('food_options.html', **trip_data)

@app.route('/places_options', methods=['POST'])
def places_options():
    trip_data = {
        'trip_type': request.form['trip_type'],
        'start_place': request.form['start_place'],
        'destination': request.form['destination'],
        'travel_dates': request.form['travel_dates'],
        'transport_mode': request.form['transport_mode'],
        'stay_type': request.form['stay_type'],
        'food_type': request.form['food_type']
    }
    
    place_type = request.form.get('place_type')
    if place_type:
        options = TRIP_DATA['places'].get(place_type, [])
        return render_template('places_display.html',
                            place_type=place_type,
                            options=options,
                            **trip_data)
    
    return render_template('places_options.html', **trip_data)

if __name__ == '__main__':
    app.run(debug=True)