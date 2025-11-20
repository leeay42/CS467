from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, abort
from bson.objectid import ObjectId
from bson import Binary
from datetime import datetime
from io import BytesIO
from app import db
from app.admin.forms import PetForm
from app.admin import admin
from app.auth.decorators import admin_access

# MongoDB collection
animals_collection = db['animals']


@admin.route('/pets', methods=['GET'])
@admin_access
def admin_dashboard():
    """Display all pets"""
    animals = list(animals_collection.find())
    return render_template('admin/dashboard.html', animals=animals)


@admin.route('/pets/new', methods=['GET', 'POST'])
@admin_access
def create_pet():
    """Create a new pet"""
    form = PetForm()
    if form.validate_on_submit():
        # Validate image is required for new pets
        if not form.public_image.data:
            flash("An image is required when creating a new pet.", "error")
            return render_template('admin/pet_form.html', form=form, title="Add New Pet")
        
        # Handle image
        image_binary = Binary(form.public_image.data.read())

        # Convert profile_date (datetime.date) to datetime.datetime
        profile_datetime = datetime.combine(form.profile_date.data, datetime.min.time()) if form.profile_date.data else None

        animal = {
            "name": form.name.data,
            "type": form.type.data,
            "availability": form.availability.data,
            "breed": form.breed.data,
            "description": form.description.data,
            "profile_date": profile_datetime,
            "disposition": form.disposition.data,
            "news_item": form.news_item.data,
            "public_image": image_binary
        }

        animals_collection.insert_one(animal)
        flash(f"Pet '{animal['name']}' created successfully!", "success")
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/pet_form.html', form=form, title="Add New Pet")


@admin.route('/pets/<id>/edit', methods=['GET', 'POST'])
@admin_access
def edit_pet(id):
    """Edit a pet"""
    animal = animals_collection.find_one({"_id": ObjectId(id)})
    if not animal:
        flash("Pet not found.", "error")
        return redirect(url_for('admin.admin_dashboard'))

    form = PetForm()

    # Pre-fill form on GET
    if request.method == 'GET':
        form.name.data = animal.get('name')
        form.type.data = animal.get('type')
        form.availability.data = animal.get('availability')
        form.breed.data = animal.get('breed')
        form.description.data = animal.get('description')
        form.disposition.data = animal.get('disposition')
        form.news_item.data = animal.get('news_item')
        # Convert datetime.datetime back to date for form display
        form.profile_date.data = animal.get('profile_date').date() if animal.get('profile_date') else None

    # Update on POST
    if form.validate_on_submit():
        # Handle image - can only replace with another image, not remove
        if form.public_image.data:
            image_binary = Binary(form.public_image.data.read())
        else:
            image_binary = animal.get('public_image')

        # Convert profile_date to datetime.datetime
        profile_datetime = datetime.combine(form.profile_date.data, datetime.min.time()) if form.profile_date.data else None

        updated_animal = {
            "name": form.name.data,
            "type": form.type.data,
            "availability": form.availability.data,
            "breed": form.breed.data,
            "description": form.description.data,
            "profile_date": profile_datetime,
            "disposition": form.disposition.data,
            "news_item": form.news_item.data,
            "public_image": image_binary
        }

        animals_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_animal})
        flash(f"Pet '{updated_animal['name']}' updated successfully!", "success")
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/pet_form.html', form=form, animal=animal, title="Edit Pet")


@admin.route('/pets/<id>/delete', methods=['POST'])
@admin_access
def delete_pet(id):
    """Delete a pet"""
    animal = animals_collection.find_one({"_id": ObjectId(id)})
    if not animal:
        flash("Pet not found.", "error")
        return redirect(url_for('admin.admin_dashboard'))

    animals_collection.delete_one({"_id": ObjectId(id)})
    flash(f"Pet '{animal['name']}' deleted successfully.", "success")
    return redirect(url_for('admin.admin_dashboard'))
