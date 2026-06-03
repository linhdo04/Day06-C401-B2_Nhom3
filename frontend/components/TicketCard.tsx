import { ArrowUpRight, Clock, MapPinned, Ticket } from "lucide-react";

import { formatCurrency } from "@/lib/format";
import type { TicketOption } from "@/lib/types";

type TicketCardProps = {
  ticket: TicketOption;
  rank: number;
};

export function TicketCard({ ticket, rank }: TicketCardProps) {
  return (
    <article className="ticket-card" data-testid="ticket-card">
      <div className="ticket-rank" aria-label={`Rank ${rank}`}>
        {rank}
      </div>

      <div className="ticket-main">
        <div className="ticket-title">
          <div>
            <p className="provider">{ticket.provider}</p>
            <h3>{ticket.operator}</h3>
          </div>
          <strong data-testid="ticket-price">{formatCurrency(ticket.price_vnd)}</strong>
        </div>

        <div className="metric-row">
          <span>
            <Clock aria-hidden="true" size={16} />
            {ticket.departure_time} → {ticket.arrival_time}
          </span>
          <span>
            <MapPinned aria-hidden="true" size={16} />
            {ticket.pickup_distance_km.toFixed(1)} km
          </span>
        </div>

        <div className="pickup-block">
          <p>{ticket.pickup_point}</p>
          <span>{ticket.pickup_address}</span>
        </div>

        <p className="rank-reason">{ticket.rank_reason}</p>

        <div className="ticket-actions">
          <a data-testid="maps-link" href={ticket.maps_url} rel="noreferrer" target="_blank">
            <MapPinned aria-hidden="true" size={16} />
            Xem Maps
          </a>
          <a data-testid="booking-link" href={ticket.booking_url} rel="noreferrer" target="_blank">
            <Ticket aria-hidden="true" size={16} />
            Đặt vé
            <ArrowUpRight aria-hidden="true" size={14} />
          </a>
        </div>
      </div>
    </article>
  );
}
