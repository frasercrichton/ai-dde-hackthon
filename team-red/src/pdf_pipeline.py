import pdfplumber
import re

# pymupdf


class PDFProcessor:

    HEADER_REGEX = r"^[A-Z]\.\s"
    SUBHEADER_REGEX = r"^[A-Z]\.\d\.\s"

    pdf_path = None

    def __init__(self, pdf_path=None):
        self.pdf_path = pdf_path
        pass

    def get_pages(self, pdf_path):
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text())
        return pages

    def remove_footnotes(self, text):
        # \n\d+  → Matches a footnote number at the start of a line.
        # .*? → Captures everything after the number (lazy match).
        # (?=\n\d+\n|$) → Stops capturing before a new page number (assumed to be on a separate line) or the end of the text.
        # Flags
        # re.DOTALL → Allows . to match newlines so the regex captures multi-line footnotes.
   
        FOOTNOTES = r'\n\d+ .*?(?=\n\d+\n|$)'

        clean_text = re.sub(FOOTNOTES, '', flags=re.DOTALL)
        return clean_text

    def remove_page_numbers(self, text):
        extrapolations_pattern = (
            r"^\s*THE\s+EXTRAPOLATIONS\s+DOCUMENT(?:\s*\n\s*|\s+)*\d+\s*$"
        )
        
        dangling_page_number = r'\n\d+\s*$'
        # r"^\s*\d+\s*$"
        clean_text = re.sub(extrapolations_pattern, "", text, flags=re.MULTILINE)
        return re.sub(dangling_page_number, "", clean_text, flags=re.MULTILINE)


    def get_main_content(self, pages_array):
        filtered_pages = []
        start_processing = False

        for page_number, text in enumerate(pages_array):
            # Skip the cover page (assumed to be the first page)
            if page_number == 0:
                continue

            # Skip the Table of Contents
            if "Table of Contents" in text:
                continue

            # Start processing after "I. Introduction"
            if not start_processing and "I. Introduction" in text:
                start_processing = True
                # Process content after "I. Introduction" within the page
                text = text.split("I. Introduction", 1)[1]

            if start_processing:
                filtered_pages.append(text.strip())

        return filtered_pages

    def group_text_by_headers(self, pages_array):
        grouped_content = []
        current_header = None
        current_text = []

        # Define the regex pattern for headers
        header_pattern = r"^[A-Z]\.\s.+"

        for page in pages_array:
            lines = page.splitlines()
            for line in lines:
                # Check if the line matches the header pattern
                if re.match(header_pattern, line.strip()):
                    # If there's an existing header, save the accumulated text
                    if current_header:
                        grouped_content.append(
                            {
                                "header": current_header,
                                "text": " ".join(current_text).strip(),
                            }
                        )
                        current_text = []  # Reset text for the new header

                    # Update the current header
                    current_header = line.strip()
                else:
                    # Accumulate text under the current header
                    if current_header:
                        current_text.append(line.strip())

        # Add the last group to the content
        if current_header:
            grouped_content.append(
                {"header": current_header, "text": " ".join(current_text).strip()}
            )

        return grouped_content

    def extract_subsections(self, grouped_data):
        subsection_pattern = r"(?P<subheader>[A-Z]\.\d+\.\s.*?\.)"  # Refined pattern
        results = []

        for group in grouped_data:
            header = group["header"]
            text = group["text"]

            subsections = []
            last_pos = 0

            matches = list(re.finditer(subsection_pattern, text, re.DOTALL))
            for idx, match in enumerate(matches):
                subheader = match.group("subheader").strip()
                start_idx = match.end()
                end_idx = matches[idx + 1].start() if idx + 1 < len(matches) else None
                subsection_text = (
                    text[start_idx:end_idx].strip()
                    if end_idx
                    else text[start_idx:].strip()
                )

                subsections.append({"subheader": subheader, "text": subsection_text})
                last_pos = match.end()

            # Handle any remaining text that does not belong to a subsection
            if last_pos < len(text.strip()):
                remaining_text = text[last_pos:].strip()
                print(remaining_text)
                if remaining_text:
                    subsections.append({"subheader": None, "text": remaining_text})

            results.append({"header": header, "subsections": subsections})

        return results

    def remove_prefix(self, regex, text):
        if text is not None:
            return re.sub(regex, "", text)
