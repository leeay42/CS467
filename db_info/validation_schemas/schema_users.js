// Validation schema for users

db.runCommand({
  "collMod": "users",       // collection name
  "validator": {
    $jsonSchema: {
      "bsonType": "object",
      "required": ["admin_access", "first_name", "last_name", "email", "password"],
      "properties": {
        "admin_access": {
          "bsonType": "bool",
          "description": "Admin access must be true or false and is required"
        },
        "first_name": {
          "bsonType": "string",
          "description": "First name must be a string and is required"
        },
        "last_name": {
          "bsonType": "string",
          "description": "Last name must be a string and is required"
        },
        "email": {
          "bsonType": "string",
          "pattern": "^.+@.+\\..+$",
          "description": "Email must be a valid email address"
        },
        "password": {
          "bsonType": "string",
          "pattern": "^[a-zA-Z0-9 ]+$",
          "description": "Password must be an alphanumeric string and is required"
        }
      }
    }
  },
  "validationLevel": "strict", // default, same validation rules to all documents
  "validationAction": "error"  // default, violations are rejected
});