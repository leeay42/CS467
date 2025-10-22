# https://stackoverflow.com/questions/40015103/upload-file-size-16mb-to-mongodb
# https://flask-wtf.readthedocs.io/en/1.0.x/quickstart/
# https://stackabuse.com/flask-form-validation-with-flask-wtf/

from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from bson import Binary
from datetime import datetime
from app import db
from app.admin.forms import PetForm

admin = Blueprint('admin', __name__)

# Get MongoDB collections
animals_collection = db['animals']


@admin.route('/admin/pets/create', methods=['GET', 'POST'])
def create_pet():
    """CREATE - Add a new pet to the database"""
    form = PetForm()

    if form.validate_on_submit():
        # Handle image upload and convert to Binary
        image_binary = None
        if form.public_image.data:
            image_file = form.public_image.data
            image_data = image_file.read()  # Read file bytes
            image_binary = Binary(image_data)  # convert to mongoDB binary format

        # Convert disposition textarea to list (split by newlines)
        disposition_list = []
        if form.disposition.data:
            disposition_list = [line.strip() for line in 
                                form.disposition.data.split('\n') if
                                line.strip()]

        # Create animal document matching schema
        animal = {
            "name": form.name.data,
            "availability": form.availability.data,
            "type": form.type.data,
            "breed": form.breed.data,
            "description": form.description.data,
            "profile_date": datetime.now(),
            "disposition": disposition_list,
            "news_item": form.news_item.data,
            "public_image": image_binary
        }

        # Insert into MongoDB
        result = animals_collection.insert_one(animal)

        if result.inserted_id:
            flash(f"Pet '{animal['name']}' created successfully!", "success")
            return redirect(url_for('admin.list_pets'))
        else:
            flash("Error creating pet. Please try again.", "error")

    return render_template('admin/create_pet.html', form=form)


@admin.route('/admin/pets/edit/<id>', methods=['GET', 'POST'])
def edit_pet(id):
    """UPDATE - Edit an existing pet"""
    form = PetForm()

    # Find the animal by ID
    animal = animals_collection.find_one({"_id": ObjectId(id)})

    if not animal:
        flash("Pet not found.", "error")
        return redirect(url_for('admin.list_pets'))

    if form.validate_on_submit():
        # Handle image upload - keep existing if no new upload
        image_binary = animal.get('public_image')
        if form.public_image.data:
            image_file = form.public_image.data
            image_data = image_file.read()
            image_binary = Binary(image_data)

        # Convert disposition textarea to list
        disposition_list = []
        if form.disposition.data:
            disposition_list = [line.strip() for line in form.disposition.data.split('\n') if line.strip()]

        # Update animal document
        updated_animal = {
            "name": form.name.data,
            "availability": form.availability.data,
            "type": form.type.data,
            "breed": form.breed.data,
            "description": form.description.data,
            "disposition": disposition_list,
            "news_item": form.news_item.data,
            "public_image": image_binary
        }

        # Update in MongoDB
        result = animals_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_animal}
        )
        if result.modified_count > 0:
            flash(f"Pet '{updated_animal['name']}' updated successfully!", "success")
        else:
            flash("No changes made.", "info")
        return redirect(url_for('admin.list_pets'))

    # Pre-fill form with existing animal data (for GET request)
    if request.method == 'GET':
        form.name.data = animal.get('name')
        form.availability.data = animal.get('availability')
        form.type.data = animal.get('type')
        form.breed.data = animal.get('breed')
        form.description.data = animal.get('description')

        # Convert disposition list to textarea format (one per line)
        if animal.get('disposition'):
            form.disposition.data = '\n'.join(animal.get('disposition'))

        form.news_item.data = animal.get('news_item')
        # Note: Can't pre-fill file upload field

    return render_template('admin/edit_pet.html', form=form, animal=animal)


@admin.route('/admin/pets/delete/<id>', methods=['POST'])
def delete_pet(id):
    """DELETE - Remove a pet from the database"""
    animal = animals_collection.find_one({"_id": ObjectId(id)})

    if not animal:
        flash("Pet not found.", "error")
        return redirect(url_for('admin.list_pets'))

    result = animals_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count > 0:
        flash(f"Pet '{animal['name']}' deleted successfully.", "success")
    else:
        flash("Error deleting pet. Please try again.", "error")

    return redirect(url_for('admin.list_pets'))


@admin.route('/admin/pets')
def list_pets():
    """LIST - Display all pets"""
    animals = list(animals_collection.find())
    return render_template('admin/pets.j2', animals=animals)
