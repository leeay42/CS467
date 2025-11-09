import base64

# Helper function to transform MongoDB pet documents into a format
# suitable for rendering in templates.
# NOTE: will try io.BytesIO or GridFS instead of base64 if slow
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



# Helper function to paginate a list of pets
# Returns a dictionary with the current page, start index, and end index
def paginate(pets_list, page=1, per_page=9):

    # Index of first item on page
    # page is the current page number
    start_index = (page - 1) * per_page
    # Index of last item on page
    end_index = min(start_index + per_page, len(pets_list))
    
    return {
        'page': page,
        'start_index': start_index,
        'end_index': end_index
    }