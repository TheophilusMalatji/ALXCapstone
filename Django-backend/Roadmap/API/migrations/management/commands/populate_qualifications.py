import pandas as pd
import re
import os
from django.core.management.base import BaseCommand
from django.core.validators import MinValueValidator, MaxValueValidator
from API.models import Education


class Command(BaseCommand):
    help = "Populate Education options (qualifications) from an Excel file."

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            required=False,
            default=os.path.join(os.path.dirname(__file__), "QualDb.xlsx"),
            help="Path to the Excel file containing education data."
        )

    def parse_nqf_level(self, nqf_level_str):
        """
        Parses an NQF level string into an integer.
        Handles formats like:
        - 'NQF Level 04'
        - 'Level TBA: Pre-2009 was L4'
        - 'Pre-2009 was L7'
        - 'L5'
        """
        if pd.isna(nqf_level_str):
            return None

        nqf_str = str(nqf_level_str).strip()

        # Common patterns
        patterns = [
            r'NQF Level (\d+)',
            r'Pre-2009 was L(\d+)',
            r'L(\d+)$',
            r'Level (\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, nqf_str)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    return None
        return None

    def handle(self, *args, **kwargs):
        excel_file_path = kwargs['path']

        education_count = 0
        skipped_count = 0

        self.stdout.write(f"📘 Reading Excel file: {excel_file_path}")

        if not os.path.exists(excel_file_path):
            self.stdout.write(self.style.ERROR(f"❗ File not found: {excel_file_path}"))
            return

        try:
            # Read the Excel file
            df = pd.read_excel(excel_file_path, sheet_name='2025 01 06')

            # Validate columns
            required_columns = ['Institution', 'Qualification', 'NQF Level']
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                self.stdout.write(self.style.ERROR(f"❗ Missing columns: {missing}"))
                return

            for index, row in df.iterrows():
                try:
                    qualification_name = row['Qualification']
                    nqf_level_str = row['NQF Level']
                    institution_name = row['Institution']

                    if pd.isna(qualification_name):
                        skipped_count += 1
                        continue

                    nqf_level = self.parse_nqf_level(nqf_level_str)
                    if nqf_level is None:
                        skipped_count += 1
                        continue

                    # Validate NQF range
                    try:
                        MinValueValidator(1)(nqf_level)
                        MaxValueValidator(10)(nqf_level)
                    except:
                        skipped_count += 1
                        continue

                    # Create or get education entry
                    education, created = Education.objects.get_or_create(
                        name=qualification_name.strip(),
                        defaults={
                            "nqf_level": nqf_level,
                            "description": f"Offered by {institution_name}" if not pd.isna(institution_name) else "",
                        }
                    )

                    if created:
                        education_count += 1
                        self.stdout.write(self.style.SUCCESS(f"✅ Added: {education.name} (NQF {nqf_level})"))

                except Exception as e:
                    skipped_count += 1
                    self.stdout.write(self.style.ERROR(f"❗ Error on row {index}: {e}"))

            self.stdout.write(self.style.SUCCESS(
                f"\n🎓 Education import completed!"
                f"\n   ✅ {education_count} new education records created."
                f"\n   ⚠️ {skipped_count} rows skipped."
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❗ Unexpected error: {e}"))
