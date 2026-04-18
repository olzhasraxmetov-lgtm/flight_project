from fpdf import FPDF

def generate_ticket_pdf(booking):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    blue_color = (0, 51, 153)
    gray_color = (128, 128, 128)

    pdf.set_draw_color(*blue_color)
    pdf.set_line_width(0.5)
    pdf.rect(10, 10, 190, 100)

    pdf.set_fill_color(*blue_color)
    pdf.rect(10, 10, 190, 20, "F")

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 20)
    pdf.text(15, 24, "BOARDING PASS")

    pdf.set_font("Arial", "B", 12)
    pdf.text(140, 23, f"REF: {booking.booking_reference}")

    pdf.set_text_color(0, 0, 0)
    passenger = booking.passengers[0]
    flight = passenger.flight_instance

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*gray_color)
    pdf.text(15, 45, "PASSENGER NAME")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.text(15, 52, f"{passenger.first_name} {passenger.last_name}".upper())

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*gray_color)
    pdf.text(120, 45, "FLIGHT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.text(120, 52, flight.flight_number)

    pdf.set_draw_color(200, 200, 200)
    pdf.line(15, 60, 195, 60)

    pdf.set_font("Arial", "B", 30)
    pdf.set_text_color(*blue_color)
    pdf.text(15, 85, f"{flight.departure_airport.code}")

    pdf.set_font("Arial", "", 20)
    pdf.set_text_color(200, 200, 200)
    pdf.text(80, 83, "----------->")

    pdf.set_font("Arial", "B", 30)
    pdf.set_text_color(*blue_color)
    pdf.text(140, 85, f"{flight.arrival_airport.code}")

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.text(15, 92, f"{flight.departure_airport.city}")
    pdf.text(140, 92, f"{flight.arrival_airport.city}")

    dep_time = flight.departure_at.strftime('%d %b %Y, %H:%M')
    pdf.set_font("Arial", "B", 10)
    pdf.text(82, 92, dep_time)

    return bytes(pdf.output())