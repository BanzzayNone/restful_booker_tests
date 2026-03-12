from fixtures.api_client import api_client
from fixtures.auth import auth_token
from fixtures.params import (
    generate_valid_bookings,
    generate_invalid_prices,
    generate_boundary_prices
)
from schemas.validators import (
    validate_booking_response,
    validate_booking_update,
    validate_auth_response
)