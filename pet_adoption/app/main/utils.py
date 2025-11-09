import base64

# Helper function to transform MongoDB pet documents into a format
# suitable for rendering in templates.
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