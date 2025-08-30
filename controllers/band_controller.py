from flask import Blueprint

band_bp =Blueprint('band_bp',__name__)

@band_bp.route('/bands', methods=['GET'])


@band_bp.route('/bands/<int:band_id>', methods=['GET'])


@band_bp.route('/bands', methods=['POST'])


@band_bp.route('/bands/<int:band_id>', methods=['PUT'])


@band_bp.route('/bands/<int:band_id>', methods=['DELETE'])
