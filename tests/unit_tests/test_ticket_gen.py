from unittest.mock import MagicMock

from app.utils.ticket_gen import generate_ticket_pdf


def test_generate_ticket_pdf_success():
    mock_booking = MagicMock()
    mock_booking.booking_reference = "ABC123"

    mock_passenger = MagicMock()
    mock_passenger.first_name = "Ivan"
    mock_passenger.last_name = "Ivanov"

    mock_flight = MagicMock()
    mock_flight.flight_number = "SU100"
    mock_flight.departure_airport.code = "SVO"
    mock_flight.departure_airport.city = "Moscow"
    mock_flight.arrival_airport.code = "JFK"
    mock_flight.arrival_airport.city = "New York"
    mock_flight.departure_at.strftime.return_value = "25 Apr 2026, 15:00"

    mock_passenger.flight_instance = mock_flight
    mock_booking.passengers = [mock_passenger]

    pdf_bytes = generate_ticket_pdf(mock_booking)

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0