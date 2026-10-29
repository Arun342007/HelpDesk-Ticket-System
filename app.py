import os
from itertools import count
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
VERSION = os.environ.get("APP_VERSION", "v1").lower()
tickets = []
ticket_ids = count(1)

@app.route("/")
def home():
    if VERSION == "v1":
        return redirect(url_for("raise_ticket"))
    if VERSION == "v3":
        return redirect(url_for("resolve_ticket"))
    return redirect(url_for("display_tickets"))

@app.route("/raise", methods=["GET", "POST"])
def raise_ticket():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        if not title or not description:
            return "Title and description are required.", 400
        ticket = {"id": next(ticket_ids), "title": title,
                  "description": description, "priority": priority,
                  "status": "Open"}
        tickets.append(ticket)
        return render_template("raise_ticket.html",
                               version=VERSION.upper(), created=ticket)
    return render_template("raise_ticket.html",
                           version=VERSION.upper(), created=None)

@app.route("/tickets")
def display_tickets():
    return render_template("tickets.html", tickets=tickets,
                           version=VERSION.upper())

@app.route("/resolve", methods=["GET", "POST"])
def resolve_ticket():
    message = None
    if request.method == "POST":
        try:
            ticket_id = int(request.form.get("ticket_id", ""))
        except ValueError:
            return "Enter a valid ticket ID.", 400
        ticket = next((t for t in tickets if t["id"] == ticket_id), None)
        if ticket is None:
            message = f"Ticket #{ticket_id} was not found."
        else:
            ticket["status"] = "Resolved"
            message = f"Ticket #{ticket_id} has been resolved."
    return render_template("resolve_ticket.html", tickets=tickets,
                           message=message, version=VERSION.upper())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
