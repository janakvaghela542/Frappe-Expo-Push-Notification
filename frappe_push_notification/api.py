import frappe

@frappe.whitelist(allow_guest=True)
def save_token(user, token, platform=None, device_name=None):
    """
    Save or update Expo token for a user.
    """
    existing = frappe.get_all("Expo Push Token", filters={"token": token})
    if existing:
        frappe.db.set_value("Expo Push Token", existing[0].name, "active", 1)
    else:
        frappe.get_doc({
            "doctype": "Expo Push Token",
            "user": user,
            "token": token,
            "platform": platform,
            "device_name": device_name,
            "active": 1
        }).insert(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success"}