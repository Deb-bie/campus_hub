from flask import Blueprint, request, jsonify # type: ignore
from ..utils.db import db
from ..models.event_model import Event
from ..services.user_profile_service import get_current_user

# blueprint
event_blueprint = Blueprint("event", __name__, url_prefix="/api/events")

# create event
@event_blueprint.route("/create", methods=["POST"])
def create_event():

    try:
        data: Event = request.get_json()

        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        auth_header = request.headers.get("Authorization")
    
        if not auth_header:
            return jsonify(
                {
                    "error": "Missing Authorization header"        
                }
            ), 401
        
        token = auth_header.replace("Bearer ", "")
        user_info = get_current_user(token)
        organizer_id = user_info.get("user_id")

        name = data['name']
        description = data['description']
        short_description = data['short_description']
        location = data['location']
        start_time = data['start_time']
        end_time = data['end_time']
        category = data['category']
        image_url = data['image_url']
        capacity = data['capacity']
        tags = data['tags']
        is_public = data['is_public']
        is_virtual = data['is_virtual']
        is_recurring = data['is_recurring']
        is_free = data['is_free']
        fee = data['fee']
        virtual_meeting_link = data['virtual_meeting_link']
        status = data['status']

        event = Event()
        event.name = name
        event.description = description
        event.short_description = short_description
        event.organizer_id = organizer_id
        event.location = location
        event.start_time = start_time
        event.end_time = end_time
        event.category = category
        event.image_url = image_url
        event.capacity = capacity
        event.tags = tags
        event.is_public =is_public
        event.is_virtual = is_virtual
        event.is_recurring = is_recurring
        event.is_free = is_free
        event.fee = fee
        event.virtual_meeting_link = virtual_meeting_link
        event.status = status

        print(event)
    

        db.session.add(event)
        db.session.commit()

        return jsonify(
            {
                'message': "successful",
                'result': event.to_json()
            }
        ), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify (
            {
                'error': str(e)
            }
        ), 400




