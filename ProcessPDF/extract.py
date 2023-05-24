from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import (
    ServiceApiException,
    ServiceUsageException,
    SdkException,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import (
    ExtractPDFOptions,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import (
    ExtractElementType,
)
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import (
    TableStructureType,
)
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

import os


def extract_pdf(dir, file, output_filepath):
    try:
        filepath = os.path.join(dir, file)

        # Initial setup, create credentials instance.
        credentials = (
            Credentials.service_account_credentials_builder()
            .from_file("./ProcessPDF/pdfservices-api-credentials.json")
            .build()
        )

        # Create an ExecutionContext using credentials
        # and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(filepath)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = (
            ExtractPDFOptions.builder()
            .with_elements_to_extract([ExtractElementType.TEXT])
            # .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES)
            .with_table_structure_format(TableStructureType.CSV)
            .build()
        )
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(output_filepath)  # zip file
    except (ServiceApiException, ServiceUsageException, SdkException):
        print("Exception encountered while executing operation")
