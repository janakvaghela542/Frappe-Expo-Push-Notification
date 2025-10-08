import frappe
from frappe_push_notification import PushClient, PushMessage, DeviceNotRegisteredError, PushServerError, PushTicketError

def send_push_notification(title, body, user=None, device_type=None, data=None):
    """
    Send a push notification to all active Expo tokens of a Frappe User.
    Example:
        send_push_notification("New Message", "Hello John!", "john@example.com", "android", {"chat_id": "123"})
    """
    tokens = frappe.get_all(
        "Expo Push Token",
        filters={"user": user, "active": 1},
        pluck="token"
    )

    if not tokens:
        frappe.log_error(f"No active Expo tokens found for user: {user}", "Push Notification")
        return

    client = PushClient()
    for token in tokens:
        try:
            message = PushMessage(
                to=token,
                title=title,
                body=body,
                sound="default",
                data=data or {}
            )
            ticket = client.publish(message)
            ticket.validate_response()
            frappe.log_error(f"Push notification sent to {token}: {ticket}", "Push Notification")
        except DeviceNotRegisteredError:
            frappe.log_error(f"Device not registered for token: {token}", "Push Notification")
            frappe.db.set_value("Expo Push Token", {"token": token}, "active", 0)
        except (PushTicketError, PushServerError) as e:
            frappe.log_error(f"Failed to send push notification to {token}: {str(e)}", "Push Notification")
        except Exception as e:
            frappe.log_error(f"Unexpected error sending push notification to {token}: {str(e)}", "Push Notification")