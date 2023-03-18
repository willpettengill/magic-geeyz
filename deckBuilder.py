import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from PIL import Image
from deckConfig import WALDS_REVENGE,ART_WIDTH,ART_HEIGHT,RAW_IMAGE_PATH,FINAL_IMAGE_PATH

def save_image(image, filename, format):
    with open(filename, 'wb') as f:
        image.save(f, format)

def load_image(image_path):
    with open(image_path, 'rb') as f:
        return Image.open(f).convert('RGBA')

def resize_image(image_path, card_width, card_height, resample=Image.BICUBIC):
    """"Resize any image to be appropriate for card art """
    image = Image.open(image_path)
    image_aspect_ratio = image.size[0] / image.size[1]
    card_aspect_ratio = card_width / card_height
    if image_aspect_ratio > card_aspect_ratio:
        new_width = card_width
        new_height = card_width / image_aspect_ratio
    else:
        new_width = card_height * image_aspect_ratio
        new_height = card_height
    resized_image = image.resize((int(new_width), int(new_height)), resample=resample)
    return resized_image, new_width, new_height


def build_card(name, image_path, mana_cost, card_type, additional_info):
    """Builds a single Magic the Gathering card with the given metadata."""
    # Set up PDF canvas
    pdf_canvas = canvas.Canvas('card.pdf', pagesize=letter)

    # Set up card template
    card_width, card_height = 2.5*inch, 3.5*inch
    card_template = pdf_canvas.rect(0, 0, card_width, card_height)

    # Load and resize card image
    card_image, x, y = resize_image(image_path, card_width, card_height)

    # Place image on card template
    pdf_canvas.drawImage(card_image, x, y)

    # Add card name
    pdf_canvas.drawString(0.5*inch, 2.75*inch, name)

    # Add mana cost
    pdf_canvas.drawString(0.5*inch, 2.5*inch, mana_cost)

    # Add card type
    pdf_canvas.drawString(0.5*inch, 2.25*inch, card_type)

    # Add any additional information
    pdf_canvas.drawString(0.5*inch, 2*inch, additional_info)

    # Save PDF file
    pdf_canvas.save()
    

def build_deck(cards):
    """Builds a PDF file containing a 3 x 3 grid of Magic the Gathering cards."""
    # Set up PDF canvas
    pdf_canvas = canvas.Canvas('magic_deck.pdf', pagesize=letter)

    # Set up card template
    card_width, card_height = 2.5*inch, 3.5*inch
    card_template = pdf_canvas.rect(0, 0, card_width, card_height)

    # Generate each card
    for i, card in enumerate(cards):
        # Load and resize card image
        card_image, x, y = resize_image(card['image_path'], card_width, card_height)

        # Place image on card template
        pdf_canvas.drawImage(card_image, x, y)

        # Add card name
        pdf_canvas.drawString(0.5*inch, 2.75)

    return pdf_canvas

''' Main Script '''

# Import config variables
walds_revenge = WALDS_REVENGE
art_width = ART_WIDTH
art_height = ART_HEIGHT
raw_image_path = RAW_IMAGE_PATH
final_image_path = FINAL_IMAGE_PATH

# Resize image and save final
resized_image, _, _ = resize_image(raw_image_path, art_width, art_height)
save_image(resized_image, final_image_path, 'JPEG')

cards = []
for card_data in [walds_revenge]:
    new_card = build_card(**card_data)
    cards.append(new_card)

deck = build_deck(cards)

# need to save deck to new file
# save_deck(deck)