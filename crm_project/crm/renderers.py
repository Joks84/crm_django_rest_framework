from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework_csv.renderers import CSVRenderer

# XLSXRenderer
# Override XLSX renderer
# Make headers and body more beautiful and pleasant to the eye

class MyCSVRenderer(CSVRenderer):
    """
    Renderer for downloading data to csv file.
    Changing the header so we can have proper column names fixed in a file.
    """
    header = [
        'First Name',
        'Last Name',
        'Email',
        'Phone',
        'City',
        'Country',
        'Company',
        'Title',
        'Lead',
    ]











