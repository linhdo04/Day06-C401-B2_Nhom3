from __future__ import annotations

from backend.app.schemas import MockTicket, Priority, TicketOption
from backend.app.agent.tools import build_booking_deeplink, build_maps_link


def rank_tickets(tickets: list[MockTicket], priority: Priority) -> list[TicketOption]:
    if priority == Priority.pickup_distance:
        ordered = sorted(tickets, key=lambda ticket: (ticket.pickup_distance_km, ticket.price_vnd))
    elif priority == Priority.time:
        ordered = sorted(tickets, key=lambda ticket: (ticket.departure_time, ticket.price_vnd))
    else:
        ordered = sorted(tickets, key=lambda ticket: (ticket.price_vnd, ticket.pickup_distance_km))

    return [to_ticket_option(ticket, priority) for ticket in ordered[:3]]


def to_ticket_option(ticket: MockTicket, priority: Priority) -> TicketOption:
    reason = {
        Priority.price: f"Gia tot nhat truoc, sau do xet diem don {ticket.pickup_distance_km:.1f} km.",
        Priority.time: f"Xuat phat som luc {ticket.departure_time}, phu hop neu muon den som.",
        Priority.pickup_distance: f"Diem don cach vi tri cua ban {ticket.pickup_distance_km:.1f} km.",
    }[priority]

    return TicketOption(
        id=ticket.id,
        provider=ticket.provider,
        operator=ticket.operator,
        from_city=ticket.from_city,
        to_city=ticket.to_city,
        date=ticket.date,
        departure_time=ticket.departure_time,
        arrival_time=ticket.arrival_time,
        price_vnd=ticket.price_vnd,
        pickup_point=ticket.pickup_point,
        pickup_address=ticket.pickup_address,
        pickup_distance_km=ticket.pickup_distance_km,
        booking_url=build_booking_deeplink(ticket.provider, ticket.id),
        maps_url=build_maps_link(ticket.pickup_address),
        rank_reason=reason,
    )
