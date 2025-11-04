from itemadapter import ItemAdapter
from copy import deepcopy
import logging
from scrapy.exporters import CsvItemExporter
from datetime import datetime

logger = logging.getLogger(__name__)

class DefaultValuePipeline:
    """
    Sets default values for fields that are declared in the Item 
    but not present in the scraped item instance.
    """
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        
        for field_name, field_meta in item.fields.items():    
            if 'default_value' in field_meta:
                if field_name not in adapter:
                    default = field_meta['default_value']

                    # IMPORTANT: Use deepcopy() to prevent mutable defaults
                    adapter[field_name] = deepcopy(default)

        return item


class CsvExportPipeline:

    """
    Exports all yielded items to a CSV file.
    This Scrapy Item Pipeline handles file creation,
    header definition, and row-by-row writing using CsvItemExporter.
    """

    def __init__(self, item_class):
        # Stores the Item class (e.g., CsvItemExport) which is used
        # to dynamically determine the fields/columns to export.
        self.item_class = item_class
        self.file = None
        self.exporter = None
        self.fields_to_export = None


    @classmethod
    def from_crawler(cls, crawler):
        from ebooks.items import CsvItemExport
        
        # Instantiate the pipeline, passing the specific Item class
        # to the __init__ method for later field discovery.
        return cls(item_class=CsvItemExport)
    

    def open_spider(self, spider):
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"output/csv/{spider.name}_{timestamp}_output.csv" 
        
        
        # Get the list of field names (keys) from the Item class.
        # This list defines the order of the columns (headers) in the CSV.
        self.fields_to_export = self.item_class.fields.keys()

        # Open the output file in binary write mode ('wb'), which is required
        # for CsvItemExporter compatibility.
        self.file = open(output_filename, 'wb')
        
        # 4. Initialize the CsvItemExporter with the file handle and field list.
        self.exporter = CsvItemExporter(
            file=self.file, 
            fields_to_export=self.fields_to_export,
            encoding='utf-8'
            )
            
        # Start the export process, which writes the header row (column names) 
        # to the CSV file based on `fields_to_export`.
        self.exporter.start_exporting()


    def close_spider(self, spider):
        
        # Signal the exporter that the export is complete (performs final file formatting).
        self.exporter.finish_exporting()
        
        # Close the output file handle to ensure all data is flushed and saved.
        self.file.close()


    def process_item(self, item, spider):
        
        # Pass the received item to the exporter, which writes it as a new row 
        # in the CSV file, matching field keys to the defined headers.
        self.exporter.export_item(item)
        
        return item
