from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

line_of_cars = {
    "change_oil": [],
    "inflate_tires": [],
    "diagnostic": []
}
last_processed_ticket = 0


class WelcomeView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return HttpResponse("<h2>Welcome to the Hypercar Service!</h2>")


class MenuView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, "tickets/menu.html")


class ProcessingView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        context = {
            "change_oil_queue": len(line_of_cars["change_oil"]),
            "inflate_tires_queue": len(line_of_cars["inflate_tires"]),
            "diagnostic_queue": len(line_of_cars["diagnostic"]),
        }
        return render(request, "tickets/processing.html", context)

    @staticmethod
    def post(request, *args, **kwargs):
        if line_of_cars["change_oil"]:
            ticket = line_of_cars["change_oil"].pop(0)
        elif line_of_cars["inflate_tires"]:
            ticket = line_of_cars["inflate_tires"].pop(0)
        elif line_of_cars["diagnostic"]:
            ticket = line_of_cars["diagnostic"].pop(0)
        else:
            ticket = None

        global last_processed_ticket
        last_processed_ticket = ticket

        return HttpResponseRedirect("next")


def next_ticket(request: HttpRequest) -> HttpResponse:
    return render(request, "tickets/next.html", context={"ticket": last_processed_ticket})


def change_oil(request: HttpRequest) -> HttpResponse:
    ticket_num = get_ticket_num()
    wait_time = len(line_of_cars["change_oil"]) * 2
    context = {
        "ticket_num": ticket_num,
        "wait_time": wait_time
    }
    line_of_cars["change_oil"].append(ticket_num)
    return render(request, "tickets/ticket.html", context)


def inflate_tires(request: HttpRequest) -> HttpResponse:
    ticket_num = get_ticket_num()
    wait_time = (len(line_of_cars["change_oil"]) * 2) + \
                (len(line_of_cars["inflate_tires"]) * 5)
    context = {
        "ticket_num": ticket_num,
        "wait_time": wait_time
    }
    line_of_cars["inflate_tires"].append(ticket_num)
    return render(request, "tickets/ticket.html", context)


def diagnostic(request: HttpRequest) -> HttpResponse:
    ticket_num = get_ticket_num()
    wait_time = (len(line_of_cars["change_oil"]) * 2) + \
                (len(line_of_cars["inflate_tires"]) * 5) + \
                (len(line_of_cars["diagnostic"]) * 30)
    context = {
        "ticket_num": ticket_num,
        "wait_time": wait_time
    }
    line_of_cars["diagnostic"].append(ticket_num)
    return render(request, "tickets/ticket.html", context)


def get_ticket_num() -> int:
    return len(line_of_cars["change_oil"]) + \
           len(line_of_cars["inflate_tires"]) + \
           len(line_of_cars["diagnostic"]) + 1
