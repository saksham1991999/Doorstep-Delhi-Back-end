payment_charge_choices = [
    ("not-charged", "Not charged"),
    ("pending", "Pending"),
    ("partially-charged", "Partially charged"),
    ("fully-charged", "Fully charged"),
    ("partially-refunded", "Partially refunded"),
    ("fully-refunded", "Fully refunded"),
    ("refused", "Refused"),
    ("cancelled", "Cancelled"),
]

transaction_kind_choices = [
    ("external", "External reference"),
    ("auth", "Authorization"),
    ("pending", "Pending"),
    ("action_to_confirm", "Action to confirm"),
    ("refund", "Refund"),
    ("refund_ongoing", "Refund in progress"),
    ("capture", "Capture"),
    ("void", "Void"),
    ("confirm", "Confirm"),
    ("cancel", "Cancel"),
]

transaction_error_choices = [
    ("incorrect_number", "incorrect_number"),
    ("invalid_number", "invalid_number"),
    ("incorrect_cvv", "incorrect_cvv"),
    ("invalid_cvv", "invalid_cvv"),
    ("incorrect_zip", "incorrect_zip"),
    ("incorrect_address", "incorrect_address"),
    ("invalid_expiry_date", "invalid_expiry_date"),
    ("expired", "expired"),
    ("processing_error", "processing_error"),
    ("declined", "declined"),
]
