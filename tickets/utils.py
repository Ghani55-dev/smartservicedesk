from django.core.mail import send_mail
from django.conf import settings

def send_ticket_notification(ticket, recipient):
    """Send an email about a ticket to the given recipient.

    The behaviour adapts based on whether the ticket has been assigned.
    - If ``ticket.assigned_to`` is truthy we send an assignment notification.
    - Otherwise we notify about ticket creation. This keeps a single helper
      compatible with every call site in ``tickets.views``.
    """

    if ticket.assigned_to:
        subject = f"New Ticket Assigned: {ticket.title}"
        message = f"""
Hi {ticket.assigned_to.get_full_name() or ticket.assigned_to.username},

You've been assigned a new support ticket.

📌 Ticket ID: {ticket.id}
📝 Title: {ticket.title}
🧾 Description: {ticket.description}
⭐ Priority: {ticket.priority}
👤 Created_by: {ticket.created_by.get_full_name() or ticket.created_by.username}
📅 Created On: {ticket.created_at.strftime('%Y-%m-%d %H:%M')}

Please log in to the ServiceDesk dashboard to view and manage the ticket.

Regards,
Smart ServiceDesk Team
        """
    else:
        # fallback for unassigned tickets (e.g. just created by a customer)
        subject = f"New Ticket Created: {ticket.title}"
        message = f"""
A new ticket has been submitted.

📌 Ticket ID: {ticket.id}
📝 Title: {ticket.title}
🧾 Description: {ticket.description}
⭐ Priority: {ticket.priority}
👤 Created_by: {ticket.created_by.get_full_name() or ticket.created_by.username}
📅 Created On: {ticket.created_at.strftime('%Y-%m-%d %H:%M')}

Please review and assign the ticket from the admin dashboard.
        """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False
    )
