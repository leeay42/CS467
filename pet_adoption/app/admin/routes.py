from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/admin/pets/create', methods=['GET', 'POST'])
def create_pet():
    # CREATE logic here
    pass

@admin.route('/admin/pets/edit/<int:id>', methods=['GET', 'POST'])
def edit_pet(id):
    # UPDATE logic here
    pass

@admin.route('/admin/pets/delete/<int:id>', methods=['POST'])
def delete_pet(id):
    # DELETE logic here
    pass