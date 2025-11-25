// Validation schema for animals

db.runCommand({
  "collMod": "animals",       // collection name
  "validator": {
    $jsonSchema: {
      "bsonType": "object",
      "required": ["name", "availability", "type", "description", "profile_date", "disposition", "news_item", "public_image"],
      "properties": {
        "name": {
          "bsonType": "string",
          "description": "Name is a string and is required"
        },
        "availability": {
          "enum": ["Not Available", "Available", "Pending", "Adopted"],
          "description": "Must be Not Available, Available, Pending or Adopted and is required"
        },
        "type": {
          "enum": ["dog", "cat", "other"],
          "description": "Must be a dog, cat or other and is required"
        },
        "breed": {
          "bsonType": "string",
          "description": "Must be a string"
        },
        "description": {
          "bsonType": "string",
          "maxLength": 300,
          "description": "Must be less than 300 characters and is required"
        },
        "profile_date": {
          "bsonType": "date",
          "description": "Must be a date and is required"
        },
        "disposition": {
          "bsonType": "array",
          "items": {
            "enum": ["Good with other animals", "Good with children", "Animal must be leashed at all times"]
          },
          "description": "Must be Good with other animals, Good with children or Animal must be leashed at all times and is required"
        },
        "news_item": {
          "bsonType": "string",
          "maxLength": 300,
          "description": "Must be less than 300 characters and is required"
        },
        "public_image": {
          "bsonType": "binData",
          "description": "Image must be binary data and is required"
        }
      }
    }
  },
  "validationLevel": "strict", // default, same validation rules to all documents
  "validationAction": "error"  // default, violations are rejected
});