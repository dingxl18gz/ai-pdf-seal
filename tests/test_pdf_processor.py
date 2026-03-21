import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pdf_processor import PdfSealProcessor


class TestPdfSealProcessorValidate(unittest.TestCase):
    def setUp(self):
        self.test_pdf = "test.pdf"
        self.test_image = "stamp.png"

    def test_validate_pdf_not_exist(self):
        with self.assertRaises(FileNotFoundError) as context:
            processor = PdfSealProcessor(
                pdf_path="not_exist.pdf",
                image_path=self.test_image,
                width=50, height=50, x=100, y=100
            )
            processor.validate()
        self.assertIn("PDF 文件不存在", str(context.exception))

    def test_validate_image_not_exist(self):
        with self.assertRaises(FileNotFoundError) as context:
            processor = PdfSealProcessor(
                pdf_path=self.test_pdf,
                image_path="not_exist.png",
                width=50, height=50, x=100, y=100
            )
            processor.validate()
        self.assertIn("印章图片不存在", str(context.exception))

    def test_validate_width_zero(self):
        with self.assertRaises(ValueError) as context:
            processor = PdfSealProcessor(
                pdf_path=self.test_pdf,
                image_path=self.test_image,
                width=0, height=50, x=100, y=100
            )
            processor.validate()
        self.assertIn("印章尺寸必须大于 0", str(context.exception))

    def test_validate_height_zero(self):
        with self.assertRaises(ValueError) as context:
            processor = PdfSealProcessor(
                pdf_path=self.test_pdf,
                image_path=self.test_image,
                width=50, height=0, x=100, y=100
            )
            processor.validate()
        self.assertIn("印章尺寸必须大于 0", str(context.exception))

    def test_validate_negative_x(self):
        with self.assertRaises(ValueError) as context:
            processor = PdfSealProcessor(
                pdf_path=self.test_pdf,
                image_path=self.test_image,
                width=50, height=50, x=-1, y=100
            )
            processor.validate()
        self.assertIn("印章坐标必须大于等于 0", str(context.exception))

    def test_validate_negative_y(self):
        with self.assertRaises(ValueError) as context:
            processor = PdfSealProcessor(
                pdf_path=self.test_pdf,
                image_path=self.test_image,
                width=50, height=50, x=100, y=-1
            )
            processor.validate()
        self.assertIn("印章坐标必须大于等于 0", str(context.exception))

    def test_validate_success(self):
        processor = PdfSealProcessor(
            pdf_path=self.test_pdf,
            image_path=self.test_image,
            width=50, height=50, x=100, y=100
        )
        result = processor.validate()
        self.assertTrue(result)


class TestPdfSealProcessorProcess(unittest.TestCase):
    def setUp(self):
        self.test_pdf = "test.pdf"
        self.test_image = "stamp.png"
        self.output_pdf = "test_output.pdf"

    def tearDown(self):
        if os.path.exists(self.output_pdf):
            os.remove(self.output_pdf)

    def test_process_creates_output(self):
        if not os.path.exists(self.test_pdf) or not os.path.exists(self.test_image):
            self.skipTest("Test files not found")

        processor = PdfSealProcessor(
            pdf_path=self.test_pdf,
            image_path=self.test_image,
            width=50, height=50, x=100, y=100
        )
        output_path = processor.process(self.output_pdf)
        self.assertTrue(os.path.exists(output_path))
        self.assertEqual(output_path, self.output_pdf)

    def test_process_default_output_name(self):
        if not os.path.exists(self.test_pdf) or not os.path.exists(self.test_image):
            self.skipTest("Test files not found")

        processor = PdfSealProcessor(
            pdf_path=self.test_pdf,
            image_path=self.test_image,
            width=50, height=50, x=100, y=100
        )
        output_path = processor.process()
        expected = "test_sealed.pdf"
        self.assertTrue(os.path.exists(output_path))
        if os.path.exists(expected):
            os.remove(expected)


if __name__ == "__main__":
    unittest.main()
