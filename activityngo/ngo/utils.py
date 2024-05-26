import re
import uuid

from activityngo.ngo import models


def generate_franchise_code():
    latest_entry = models.Ngo.objects.order_by("-franchise_code").first()

    if latest_entry:
        numeric_part = int(latest_entry.franchise_code[2:])

        if numeric_part < 9999:
            incremented_numeric_part = numeric_part + 1
            formatted_numeric_part = str(incremented_numeric_part).zfill(4)
        else:
            formatted_numeric_part = False
        new_franchise_code = "AP" + formatted_numeric_part
    else:
        new_franchise_code = "AP0001"

    return new_franchise_code


def generate_slug_from_uuid():
    # Step 1: Generate a UUID
    generated_uuid = uuid.uuid4()

    # Step 2: Convert UUID to a string
    uuid_string = str(generated_uuid)

    # Step 3: Create the slug from the UUID string
    slug = re.sub(r"[^a-z0-9]", "-", uuid_string.lower())
    slug = re.sub(r"--+", "-", slug).strip("-")

    return slug
