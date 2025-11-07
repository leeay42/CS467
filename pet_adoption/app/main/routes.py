# https://www.mongodb.com/docs/manual/tutorial/query-documents/
# https://www.geeksforgeeks.org/python/multi-value-query-parameters-with-flask/
# https://www.geeksforgeeks.org/python/how-to-implement-filtering-sorting-and-pagination-in-flask/
# https://stackoverflow.com/questions/18214612/how-to-access-app-config-in-a-blueprint
# debugged single pet GET with claude.ai

from flask import render_template, request
import base64
from bson.objectid import ObjectId
from app import db
from app.main import main

# Get MongoDB collections
animals_collection = db['animals']

# NOTE: move over to utils
# helper to make pet documents from db usable
def prep_pet(pet):
    return {
        "id": str(pet['_id']),
        "pet_name": pet['name'],
        "availability": pet['availability'],
        "type": pet['type'],
        "breed": pet['breed'],
        "description": pet['description'],
        "profile_date": pet['profile_date'].strftime("%m/%d/%Y"),
        "disposition": pet['disposition'],
        "news_item": pet['news_item'],
        # images are binData, converted to string for URL
        "images": f"data:image/jpeg;base64,{base64.b64encode(pet['public_image']).decode('utf-8')}"
    }


@main.route("/")
def index():
    # NOTE: highlights go here
    return render_template('index.html')


# browse through all pets
# used browse.html
@main.route('/browse', methods=['GET'])
def browse(): 
    all_pets = list(animals_collection.find()) 
    prepped_pets = [prep_pet(pet) for pet in all_pets]

    # Pagination for 3 x 3 grid of pet profiles
    page = int(request.args.get('page', 1))         # {{ current_page }}, return 1 as default if none
    per_page = 9    # total profiles for page
    start_index = (page - 1) * per_page             # 1st profile to show on page
    # last profile to show on page
    # min to avoid going past the end of profiles
    end_index = min(start_index + per_page, len(prepped_pets))  
    
    return render_template('browse.html', 
                            data=prepped_pets,
                            current_page=page,
                            start_index=start_index,
                            end_index=end_index)


# Search for pets using selected categories
# used search.html
@main.route('/search', methods=['GET'])  
def search():  
    # Get filter parameters from search.html
    selected_types = request.args.getlist('types[]')
    selected_breeds = request.args.getlist('breeds[]')
    selected_availability = request.args.getlist('availability[]')
    # PLACEHOLDER: make one for DATE
        
    # Build json query filter for mongoDB
    query = {}
    if selected_types:
        query['type'] = {'$in': selected_types}
    if selected_breeds:
        query['breed'] = {'$in': selected_breeds}
    if selected_availability:
        query['availability'] = {'$in': selected_availability}
    
    # Get all pets matching filters from mongodb
    pets = list(animals_collection.find(query))
    prepped_pets = [prep_pet(pet) for pet in pets]      # use helper above
    
    # Get all unique breeds for filter display
    all_breeds = animals_collection.distinct('breed')

    # Pagination for 3 x 3 grid of pet profiles
    page = int(request.args.get('page', 1))         # {{ current_page }}, return 1 as default if none
    per_page = 9        # total profiles for page
    start_index = (page - 1) * per_page             # 1st profile to show on page
    # last profile to show on page
    # min to avoid going past the end of profiles
    end_index = min(start_index + per_page, len(prepped_pets))
    
    return render_template('search.html',
                        results=prepped_pets, 
                        breeds=sorted(all_breeds),
                        selected_types=selected_types,
                        selected_breeds=selected_breeds,
                        selected_availability=selected_availability,
                        current_page=page,
                        start_index=start_index,
                        end_index=end_index)

# STILL NEED TO VERIFY
# get detail about a single pet
# will link from "View Profile"
# search.html and browse.html to profile.html
@main.route('/pet_detail/<string:pet_id>', methods=['GET'])  
def pet_detail(pet_id):
    
    try:
        # need to change string to ObjectID for MongoDB
        pet = animals_collection.find_one({'_id': ObjectId(pet_id)})
        if pet:
            prepped_pet = prep_pet(pet)     # use helper above
            return render_template('pet_detail.html', pet=prepped_pet)

        else:
            # pet does not exist in db
            return f"No pet found with ID: {pet_id}", 404
    # other client errors
    except Exception as e:
        return f"Cannot GET: {pet_id}, Error: {str(e)}", 400

