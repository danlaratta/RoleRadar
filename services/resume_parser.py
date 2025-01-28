import fitz

class ResumeParser:
    @staticmethod
    def parse_resume():
        # Open the resume PDF file
        doc = fitz.open('asset/resume.pdf')

        # Extract data from resume in blocks/sections
        page = doc.load_page(0)  # resume is only 1 page so gets that page
        blocks = page.get_text('blocks')  # extract the text blocks
        text = '\n'.join(block[4].strip() for block in blocks if block[4].strip())
        return text

