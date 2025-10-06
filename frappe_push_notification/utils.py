import frappe
from frappe_push_notification import PushClient, PushMessage, DeviceNotRegisteredError, PushTicketError, PushServerError
import os
import requests
from requests.exceptions import ConnectionError, HTTPError

# Optional session with Expo token
session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {os.getenv('EXPO_TOKEN')}",
    "accept": "application/json",
    "accept-encoding": "gzip, deflate",
    "content-type": "application/json",
})

def send_push(token, message, extra=None):
    client = PushClient(session=session)
    try:
        ticket = client.publish(PushMessage(to=token, body=message, data=extra))
        ticket.validate_response()
        return ticket
    except DeviceNotRegisteredError:
        frappe.get_doc("Push Token", {"token": token}).db_set("active", 0)
    except (PushTicketError, PushServerError, ConnectionError, HTTPError) as e:
        frappe.log_error(str(e), "Push Notification Error")
        return None

def send_todo_push(doc, method=None):
    """Automatically send push when a ToDo is created"""
    tokens = [p.token for p in frappe.get_all("Push Token", filters={"active": 1}, pluck="token")]
    for token in tokens:
        send_push(token, f"New ToDo: {doc.title}", extra={"doctype": doc.doctype, "name": doc.name})
