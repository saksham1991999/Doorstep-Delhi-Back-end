order_status_choices = [
    ("draft", "Draft"),
    ("unconfirmed", "Unconfirmed"),
    ("unfulfilled", "Unfulfilled"),
    ("partially_fulfilled", "Partially fulfilled"),
    ("partially_returned", "Partially returned"),
    ("returned", "Returned"),
    ("fulfilled", "Fulfilled"),
    ("canceled", "Canceled"),
]

order_event_type_choices = [
    ("draft_created", "The draft order was created"),
    ("draft_created_from_replace", "The draft order with replace lines was created"),
    ("draft_added_products", "Some products were added to the draft order"),
    ("draft_removed_products", "Some products were removed from the draft order"),
    ("placed", "The order was placed"),
    ("placed_from_draft", "The draft order was placed"),
    ("oversold_items", "The draft order was placed with oversold items"),
    ("canceled", "The order was canceled"),
    ("order_marked_as_paid", "The order was manually marked as fully paid"),
    ("order_fully_paid", "The order was fully paid"),
    ("order_replacement_created", "The draft order was created based on this order."),
    ("order_discount_added", "New order discount applied to this order."),
    (
        "order_discount_automatically_updated",
        "Order discount was automatically updated after the changes in order.",
    ),
    ("order_discount_updated", "Order discount was updated for this order."),
    ("order_discount_deleted", "Order discount was deleted for this order."),
    ("order_line_discount_updated", "Order line was discounted."),
    ("order_line_discount_removed", "The discount for order line was removed."),
    ("updated_address", "The address from the placed order was updated"),
    ("email_sent", "The email was sent"),
    ("confirmed", "Order was confirmed"),
    ("payment_authorized", "The payment was authorized"),
    ("payment_captured", "The payment was captured"),
    ("external_service_notification", "Notification from external service"),
    ("payment_refunded", "The payment was refunded"),
    ("payment_voided", "The payment was voided"),
    ("payment_failed", "The payment was failed"),
    ("invoice_requested", "An invoice was requested"),
    ("invoice_generated", "An invoice was generated"),
    ("invoice_updated", "An invoice was updated"),
    ("invoice_sent", "An invoice was sent"),
    ("fulfillment_canceled", "A fulfillment was canceled"),
    ("fulfillment_restocked_items", "The items of the fulfillment were restocked"),
    ("fulfillment_fulfilled_items", "Some items were fulfilled"),
    ("fulfillment_refunded", "Some items were refunded"),
    ("fulfillment_returned", "Some items were returned"),
    ("fulfillment_replaced", "Some items were replaced"),
    ("tracking_updated", "The fulfillment's tracking code was updated"),
    ("note_added", "A note was added to the order"),
    ("reaching_pickup_point", "Order is reaching Pickup Point"),
    ("reached_pickup_point", "Order has reached Pickup Point"),
    ("picked_up_from_pickup_point", "Order has been picked up from Pickup Point"),
    ("other", "An unknown order event containing a message"),
]

voucher_type_choices = [
    ("entire_order", "Entire order"),
    ("shipping", "Shipping"),
    ("specific_product", "Specific products, collections and categories"),
]

discout_value_type_choices = [
    ("fixed", "fixed"),
    ("percentage", "%"),
]


main_order_event_type_choices = [
    ("draft_created", "The draft order was created"),
    ("placed", "The order was placed"),
    ("canceled", "The order was canceled"),
    ("confirmed", "Order was confirmed"),
    ("payment_captured", "The payment was captured"),
    ("payment_failed", "The payment was failed"),
    ("reaching_pickup_point", "Order is reaching Pickup Point"),
    ("reached_pickup_point", "Order has reached Pickup Point"),
    ("picked_up_from_pickup_point", "Order has been picked up from Pickup Point"),
    ("payment_refunded", "The payment was refunded"),
    ]
