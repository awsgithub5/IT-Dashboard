from PIL import Image, ImageDraw, ImageFont
import os
import tempfile
# import PyPDF2 as pdf2
# from PyPDF2 import PdfWriter, PdfReader



def date_range(start_date, end_date):
    # Convert start and end dates to datetime objects

    # Extract month and year from start and end dates
    start_month_year = start_date.strftime("%B %Y")
    end_month_year = end_date.strftime("%B %Y")

    # Return date range string
    return f"{start_month_year} to {end_month_year}"

# def remove_page(pdf_path):
#     pages_to_delete = [1] 
#     infile = PdfReader(pdf_path, 'rb')
#     output = PdfWriter()

#     for i in range(len(infile.pages)):
#         if i not in pages_to_delete:
#             p = infile.pages[i]
#             output.add_page(p)

#     with open(pdf_path, 'wb') as f:
#         output.write(f)
#         return pdf_path

def _create_image( message, font, fontColor,img_path,landscape=False):
    if landscape:
        W= int(3508/2.92)
        H= int(2480/2.92)
    else:
        W= int(2480/2.92)
        H= int(3508/3.2)

    im = Image.open(img_path)
    
    resized_image = im.resize((W, H))
    draw = ImageDraw.Draw(resized_image)
    _, _, w, h = draw.textbbox((0, 30), message[0], font=font)
    draw.text(((W-w)/2, (H-h)/2), message[0], font=font, fill=fontColor)
    
    font = ImageFont.load_default(20)
    _, _, w, h = draw.textbbox((0, -120), message[1], font=font)
    draw.text(((W-w)/2, (H-h)/2), message[1], font=font, fill=fontColor)

    font = ImageFont.load_default(25)
    _, _, w, h = draw.textbbox((0, -60), message[2], font=font)
    draw.text(((W-w)/2, (H-h)/2), message[2], font=font, fill=fontColor)
    

    # o_img_pth=r"D:\JD_Support\JD_dashboard\Final_dash\logo.png"
    # over_img=Image.open(o_img_pth)
    # ow,oh=over_img.size
    # over_img=over_img.resize((int(ow/3.5),int(oh/3.5)))
    # resized_image.paste(over_img,(720,20))

    return resized_image

# def _image_to_pdf(image, pdf_path):
#     # Save image to temporary PDF file
#     pdf_filename = tempfile.mkstemp(suffix='.pdf')[1]
#     image.save(pdf_filename, "PDF" ,resolution=100.0)
    
#     with open (pdf_path, "rb") as f:
#         pdf = pdf2.PdfReader(f)
#         merger = pdf2.PdfMerger()  
#         merger.append(pdf2.PdfReader(open(pdf_filename, "rb")))
#         merger.append(pdf)
#         output_filename = f"{os.path.splitext(pdf_path)[0]}_.pdf"
#         with open(output_filename, "wb") as outfile: 
#             merger.write(outfile)
#             return output_filename

def add_img_to_pdf(img_path,pdf_path,message):
    myFont = ImageFont.load_default(50)
    myImage = _create_image(message, myFont, 'black',img_path,False)
    path=_image_to_pdf(myImage,pdf_path)
    return path

# from spire.doc import *
# from spire.doc.common import *

# def add_offset_colour(doc_path):
    
#     # Create a Document object
#     document = Document()
#     # Load a Word document
#     document.LoadFromFile(doc_path)
#     # Get the document's background
#     background = document.Background
#     # Set the background type as Color
#     background.Type = BackgroundType.Color
#     # Set the background color
#     background.Color = Color.get_AliceBlue()
#     #save the resulting document
#     document.SaveToFile(doc_path, FileFormat.Docx2016)
#     return doc_path

base_images = ["images/cover_pages/base_image_1.jpg"]

def generate_cover(start_date, end_date, tenant_name, pdf_path, application="Worksoft CTM"):
    # message = ["worksoft", "date_str", "tenet_name"]
    # offset_doc = add_offset_colour(doc_path)
    date_str = date_range(start_date, end_date)
    message = [application, date_str, tenant_name]
    new_pdf_path = add_img_to_pdf(base_images[0], pdf_path, message)
    # final_df_path = remove_page(new_pdf_path)
    # remove old pdf
    if os.path.exists(pdf_path):
       os.remove(pdf_path)
    
    return new_pdf_path