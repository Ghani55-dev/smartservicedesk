from django.shortcuts import render, redirect
from .forms import TicketForm, AssignTicketForm, UpdateStatusForm
from .models import Ticket
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .utils import send_ticket_notification
from .models import TicketActivity
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.http import HttpResponseForbidden
@login_required
def create_ticket(request):
    if request.user.role != 'customer':
        return HttpResponseForbidden("Only customers are allowed to create tickets.")

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()

            # Notify admin (update email accordingly)
            send_ticket_notification(
                subject="New Ticket Created",
                message=f"A new ticket '{ticket.title}' has been created by {request.user.username}.",
                recipient="ganaganiganesh5268@gmail.com"
            )
            messages.success(request, "✅ Ticket submitted successfully. Our support team will address it shortly.")
            return redirect('ticket_list')
    else:
        form = TicketForm()
    
    return render(request, 'tickets/create_ticket.html', {'form': form})
@login_required
def ticket_list(request):
    user = request.user
    if user.role == 'admin':
        tickets = Ticket.objects.all()
    elif user.role == 'agent':
        tickets = Ticket.objects.filter(assigned_to=user)
    else:
        tickets = Ticket.objects.filter(created_by=user)
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


from django.contrib import messages

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    assign_form = None
    status_form = None

    if request.method == 'POST':
        # Admin assigns ticket
        if request.user.role == 'admin':
            assign_form = AssignTicketForm(request.POST, instance=ticket, prefix="assign")
            if assign_form.is_valid():
                assign_form.save()

                if ticket.assigned_to:
                    # ✅ Fixed function call
                    send_ticket_notification(ticket, ticket.assigned_to.email)

                messages.success(request, "✅ Ticket assigned successfully!")
                return redirect('ticket_detail', ticket_id=ticket.id)
            else:
                messages.error(request, "❌ Failed to assign ticket. Please try again.")

        # Agent updates ticket status
        elif request.user.role == 'agent' and ticket.assigned_to == request.user:
            status_form = UpdateStatusForm(request.POST, instance=ticket, prefix="status")
            if status_form.is_valid():
                updated_ticket = status_form.save()

                # ✅ Fixed function call
                send_ticket_notification(updated_ticket, updated_ticket.created_by.email)

                TicketActivity.objects.create(
                    ticket=ticket,
                    user=request.user,
                    action=f"status updated to '{ticket.status}'" if request.user.role == 'agent'
                    else f"assigned to {ticket.assigned_to.username if ticket.assigned_to else 'n/a'}"
                )

                messages.success(request, "✅ Ticket status updated successfully!")
                return redirect('ticket_detail', ticket_id=ticket.id)
            else:
                messages.error(request, "❌ Failed to update status. Please check and try again.")

    else:
        if request.user.role == 'admin':
            assign_form = AssignTicketForm(instance=ticket, prefix="assign")
        if request.user.role == 'agent' and ticket.assigned_to == request.user:
            status_form = UpdateStatusForm(instance=ticket, prefix="status")

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'assign_form': assign_form,
        'status_form': status_form,
    })



@login_required
def recent_activities(request):
    activities = TicketActivity.objects.select_related('ticket', 'user').order_by('-created_at')[:10]
    data = [
        {
            'ticket_id': activity.ticket.id,
            'action': activity.action,
            'user': activity.user.username if activity.user else 'Unknown',
            'time_ago': timesince(activity.created_at) + " ago"
        }
        for activity in activities
    ]
    return JsonResponse({'activities': data})
