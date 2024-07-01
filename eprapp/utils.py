

import datetime
import qrcode
from PIL import Image, ImageDraw, ImageFont

def create_ticket(ticket_data, ticket_template, margin=10, font_path="JKMapp/static/Roboto-Medium.ttf"):
    """
    Create a single ticket with QR code and text information.

    Parameters:
    - ticket_data: Dictionary containing ticket-specific data such as date, time, location, price, and number.
    - ticket_template: PIL Image object representing the ticket template.
    - margin: Margin between tickets on the canvas. Default is 10 pixels.
    - font_path: File path to the font used for text. Default is "JKMapp/static/Roboto-Medium.ttf".
    """
    # Get ticket data
    date = ticket_data.get('date', '')
    time = ticket_data.get('time', '')
    location = ticket_data.get('location', '')
    price = ticket_data.get('price', '')
    ticket_number = ticket_data.get('number', '')

    # Define text information
    text_info = [
        (f"{date}", (410, 550)),
        (f"{time}", (410, 620)),
        (f"Rs. {price}", (410, 690)),
        (f"{location}", (410, 760)),
        (f"Ticket Number: {ticket_number}", (210, 490))
    ]

    # Create a copy of the ticket template
    ticket_copy = ticket_template.copy()

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=15,
        border=4,
    )
    qr_data = ticket_data.get('qr_data', '')
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Paste QR code onto ticket template copy
    qr_width, qr_height = qr_img.size
    qr_x_offset = ticket_copy.width // 2
    qr_y_offset = 0
    ticket_copy.paste(qr_img, (qr_x_offset, qr_y_offset))

    # Draw text on ticket template copy
    draw = ImageDraw.Draw(ticket_copy)
    font_size = 60
    color = (255, 0, 0)
    font = ImageFont.truetype(font_path, size=font_size)
    for text, position in text_info:
        draw.text(position, text, fill=color, font=font)

    return ticket_copy

def create_tickets_2(number, start_number, ticket_template, ticket_data_list, margin=10):
    """
    Create multiple tickets with QR codes and text information.

    Parameters:
    - number: Number of tickets to create.
    - start_number: Starting number for ticket numbering.
    - ticket_template: PIL Image object representing the ticket template.
    - ticket_data_list: List of dictionaries containing ticket-specific data for each ticket.
    - margin: Margin between tickets on the canvas. Default is 10 pixels.

    Returns:
    - canvas: PIL Image object containing all the tickets.
    """
    # Create the canvas
    ticket_width, ticket_height = ticket_template.size
    total_width = ticket_width
    total_height = number * (ticket_height + margin)
    canvas = Image.new('RGB', (total_width, total_height), color='white')

    # Paste tickets onto the canvas
    y_offset = 0
    for i in range(start_number, number + start_number):
        ticket_data = ticket_data_list[i - start_number]
        ticket = create_ticket(ticket_data, ticket_template)
        canvas.paste(ticket, (0, y_offset))
        y_offset += ticket_height + margin

    return canvas




def create_tickets(number, start_number, ticket_template, margin=10, data_prefix="JKM2024", font_path="JKMapp/static/Roboto-Medium.ttf"):
    # Define prerequisites and variables
    font_size = 60
    color = (255, 0, 0)
    text_info = []

    # Get current date and time
    current_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    formatted_date = current_datetime.strftime("%d-%m-%Y")
    formatted_time = current_datetime.strftime("%H:%M:%S")
    location = "Ghaziabad"

    text_info.append((f"{formatted_date}", (410, 550)))
    text_info.append((f"{formatted_time}", (410, 620)))
    text_info.append(("Rs.100", (410, 690)))
    text_info.append((f"{location}", (410, 760)))

    # Create the canvas
    ticket_width, ticket_height = ticket_template.size
    total_width = ticket_width
    total_height = number * (ticket_height + margin)
    canvas = Image.new('RGB', (total_width, total_height), color='white')

    y_offset = 0
    
    for i in range(start_number,number + start_number):
        # Make a copy of the ticket template for each ticket
        ticket_template_copy = ticket_template.copy()

        qr = qrcode.QRCode(
            version=1,
            box_size=15,
            border=4,
        )
        qr_data = f'{data_prefix}_{i}'
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Paste the QR code onto the ticket template copy    
        qr_width, qr_height = qr_img.size
        qr_x_offset = ticket_width // 2
        qr_y_offset = y_offset
        ticket_template_copy.paste(qr_img, (qr_x_offset, qr_y_offset))

        # Draw text on the ticket template copy
        draw = ImageDraw.Draw(ticket_template_copy)
        font = ImageFont.truetype(font_path, size=font_size)
        for text, position in text_info:
            draw.text(position, text, fill=color, font=font)

        # Add ticket number to text information
        ticket_number = f"Ticket Number: {i}"
        draw.text((210, 490), ticket_number, fill=color, font=font)

        # Paste the ticket template copy onto the canvas
        canvas.paste(ticket_template_copy, (0, (ticket_height + margin) * (i - start_number)))

    # Return the canvas
    return canvas



def generate_single_pass(info, text_info, ticket_template, font_path="JKMapp/static/Roboto-Medium.ttf"):
    """
    Generate a single pass with QR code and text information.

    Args:
        info (dict): Dictionary containing user information and ticket details.
            Expected keys: 'username', 'date', 'time', 'total_tickets', 'tickets_in_pass'
        text_info (dict): Dictionary containing text information and their positions.
            Keys are text strings and values are tuples with (x, y) positions.
        ticket_template (Image): An Image object representing the ticket template.
        font_path (str): Path to the font file.

    Returns:
        Image: The generated pass image.
    """
    # Define variables
    font_size = 60
    color = (255, 0, 0)

    # Extract information from the dictionary
    username = info['username']
    date = info['date']
    time = info['time']
    total_tickets = info['total_tickets']
    tickets_in_pass = info['tickets_in_pass']
    location = info.get('location', 'Ghaziabad')  # Default to Faridabad if not provided

    # Format date and time
    formatted_date = date.strftime("%d-%m-%Y")
    formatted_time = time.strftime("%H:%M:%S")

    # Create the pass
    ticket_template_copy = ticket_template.copy()

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=15,
        border=4,
    )
    qr_data = f'{username}_{date.strftime("%d%m")}_{total_tickets}_{tickets_in_pass}'
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Position and paste the QR code onto the ticket template copy
    qr_width, qr_height = qr_img.size
    qr_x_offset = (ticket_template_copy.width) // 2  # Center the QR code horizontally
    qr_y_offset = 0  # Adjust this value as needed
    ticket_template_copy.paste(qr_img, (qr_x_offset, qr_y_offset))

    # Draw text on the ticket template copy
    draw = ImageDraw.Draw(ticket_template_copy)
    font = ImageFont.truetype(font_path, size=font_size)
    for text, position in text_info.items():
        draw.text(position, text, fill=color, font=font)

    # Return the ticket
    return ticket_template_copy




