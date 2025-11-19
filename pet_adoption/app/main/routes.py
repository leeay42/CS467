# https://www.mongodb.com/docs/manual/tutorial/query-documents/
# https://www.geeksforgeeks.org/python/multi-value-query-parameters-with-flask/
# https://www.geeksforgeeks.org/python/how-to-implement-filtering-sorting-and-pagination-in-flask/
# https://stackoverflow.com/questions/18214612/how-to-access-app-config-in-a-blueprint
# debugged single pet GET with claude.ai

from flask import render_template, request
from bson.objectid import ObjectId
from datetime import datetime
from app import db
from app.main import main
from app.main.utils import prep_pet, paginate

# Get MongoDB collections
animals_collection = db['animals']

# landing page
@main.route("/")
def index():
    # Get the 4 newest pets (sorted by profile_date descending)
    newest_pets_cursor = animals_collection.find({ 'availability' : "Available" }).sort('profile_date', -1).limit(4)
    
    # Transform pets and wrap images in a list
    newest_pets = []
    for pet in newest_pets_cursor:
        pet_data = prep_pet(pet)
        # Wrap the single image string in a list
        pet_data['images'] = [pet_data['images']]
        newest_pets.append(pet_data)
    return render_template('index.html', newest_pets=newest_pets)


# renders donate.html
@main.route("/donate")
def donate():
    return render_template('donate.html')

# renders contact.html
@main.route("/contact")
def contact():
    return render_template('contact.html')


# browse through all pets
# used browse.html
@main.route('/browse', methods=['GET'])
def browse(): 
    # get all pets sorted by descending order (newest first)
    all_pets = list(animals_collection.find().sort('profile_date', -1)) 
    prepped_pets = [prep_pet(pet) for pet in all_pets]

    # Pagination for 3 x 3 grid of pet profiles
    page = int(request.args.get('page', 1))         # {{ current_page }}, return 1 as default if none
    pagination = paginate(prepped_pets, page=page, per_page=9)
    
    return render_template('browse.html', 
                            data=prepped_pets,
                            current_page=pagination['page'],
                            start_index=pagination['start_index'],
                            end_index=pagination['end_index'])


# Search for pets using selected categories
# used search.html
@main.route('/search', methods=['GET'])  
def search():  

    # Get filter parameters from search.html
    selected_types = request.args.getlist('types[]')
    selected_breeds = request.args.getlist('breeds[]')
    selected_availability = request.args.getlist('availability[]')
    date_from = request.args.get('date_from')  # Format: YYYY-MM-DD
    date_to = request.args.get('date_to')      # Format: YYYY-MM-DD
        
    # Build json query filter for mongoDB
    query = {}
    if selected_types:
        query['type'] = {'$in': selected_types}
    if selected_breeds:
        query['breed'] = {'$in': selected_breeds}
    if selected_availability:
        query['availability'] = {'$in': selected_availability}
    
    # Date range filter for profile_date
    if date_from or date_to:
        query['profile_date'] = {}
        if date_from:
            query['profile_date']['$gte'] = datetime.strptime(date_from, '%Y-%m-%d')
        if date_to:
            query['profile_date']['$lte'] = datetime.strptime(date_to, '%Y-%m-%d')
    
    # Get all pets matching filters from mongodb
    pets = list(animals_collection.find(query))
    prepped_pets = [prep_pet(pet) for pet in pets] 
    
    # Get all unique breeds for filter display
    all_breeds = animals_collection.distinct('breed')

    # Pagination for 3 x 3 grid of pet profiles
    page = int(request.args.get('page', 1))         # {{ current_page }}, return 1 as default if none
    pagination = paginate(prepped_pets, page=page, per_page=9)

    return render_template('search.html',
                        results=prepped_pets, 
                        breeds=sorted(all_breeds),
                        selected_types=selected_types,
                        selected_breeds=selected_breeds,
                        selected_availability=selected_availability,
                        date_from=date_from,
                        date_to=date_to,
                        current_page=pagination['page'],
                        start_index=pagination['start_index'],
                        end_index=pagination['end_index'])

# get detail about a single pet
# from index.html, search.html and browse.html to profile.html
@main.route('/pet_detail/<string:pet_id>', methods=['GET'])  
def pet_detail(pet_id):
    
    try:
        # need to change string to ObjectID for MongoDB
        pet = animals_collection.find_one({'_id': ObjectId(pet_id)})
        if pet:
            prepped_pet = prep_pet(pet)

            # Find 5 related available pets based on same type
            related_query = {
                '_id': {'$ne': ObjectId(pet_id)},  # Exclude current pet
                'type': pet['type'],
                'availability': 'Available'
            }
            related_pets_cursor = animals_collection.find(related_query).limit(5)
            related_pets = [prep_pet(p) for p in related_pets_cursor]
            
            # Wrap images in a list for html compatibility
            for related_pet in related_pets:
                related_pet['images'] = [related_pet['images']]
            
            return render_template('profile.html', pet=prepped_pet, related_pets=related_pets)

        else:
            # pet does not exist in db
            return f"No pet found with ID: {pet_id}", 404
    # other client errors
    except Exception as e:
        return f"Cannot GET: {pet_id}, Error: {str(e)}", 400
