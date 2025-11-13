from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print('Main index route hit')
    newest_pets = [
        {
            'id': 1,
            'pet_name': 'Buddy',
            'breed': 'Golden Retriever',
            'availability': 'Available',
            'description': 'Friendly and playful.',
            'images': ['/static/placeholder.jpg']
        },
        {
            'id': 2,
            'pet_name': 'Mittens',
            'breed': 'Tabby Cat',
            'availability': 'Adopted',
            'description': 'Loves naps and cuddles.',
            'images': ['/static/placeholder.jpg']
        }
    ]
    return render_template('index.html', newest_pets=newest_pets)

@main.route('/browse')
def browse():
    print('Browse route hit')
    return render_template('browse.html')

@main.route('/search')
def search():
    print('Search route hit')
    return render_template('search.html')

@main.route('/pets')
def pets():
    print('/pets route hit')
    return 'Pets route is working!'

@main.route('/pet/<int:pet_id>')
def highlight(pet_id):
    print(f'Highlight route hit for pet {pet_id}')
    # Add your logic to fetch and display pet details
    return render_template('pet_detail.html', pet_id=pet_id)

@main.route('/donate')
def donate():
    print('Donate route hit')
    return render_template('donate.html')

@main.route('/contact')
def contact():
    print('Contact route hit')
    return render_template('contact.html')

@main.route('/test-db')
def test_db():
    from app import db
    try:
        # Try to list collections
        collections = db.list_collection_names()
        return f"Connected! Collections: {collections}"
    except Exception as e:
        return f"Database error: {str(e)}"