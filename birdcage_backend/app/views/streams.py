from flask import Blueprint, request, jsonify
from app.models.streams import Stream
from app.decorators import admin_required
from playhouse.shortcuts import model_to_dict

streams_blueprint = Blueprint('streams', __name__)


def get_streams_list():
    streams = Stream.select()
    return streams


@streams_blueprint.route('/api/streams', methods=['GET'])
def get_streams():
    streams = get_streams_list()
    return jsonify([model_to_dict(s) for s in streams])


@streams_blueprint.route('/api/streams', methods=['POST'])
@admin_required
def create_stream():
    data = request.get_json()

    stream = Stream.create(
        name=data['name'],
        address=data['address'],
        protocol=data['protocol'],
        transport=data.get('transport')
    )

    return jsonify({"message": "Stream created successfully. ID: {}".format(stream.id)})


@streams_blueprint.route('/api/streams/<int:stream_id>', methods=['PUT'])
@admin_required
def update_stream(stream_id):
    data = request.get_json()

    stream = Stream.get_by_id(stream_id)
    stream.name = data['name']
    stream.address = data['address']
    stream.protocol = data['protocol']
    stream.transport = data.get('transport')
    stream.save()

    return jsonify({"message": "Stream updated successfully."})


@streams_blueprint.route('/api/streams/<int:stream_id>', methods=['DELETE'])
@admin_required
def delete_stream(stream_id):

    stream = Stream.get_by_id(stream_id)
    stream.delete_instance()

    return jsonify({"message": "Stream deleted successfully."})
