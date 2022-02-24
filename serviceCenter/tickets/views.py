from django.views import View
from django.shortcuts import render, redirect
from django.http.response import HttpResponse


class WelcomeView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
        # return HttpResponse('')


class MenuView(View):
    template_name = 'menu.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


counter = 1
line_of_cars = {'change_oil': [], 'inflate_tires': [], 'diagnostic': []}
next_ticket = -1


def get_ticket():
    global counter
    t_no = counter
    counter += 1
    return t_no


def oil_time():
    return len(line_of_cars['change_oil']) * 2


def tire_time():
    return oil_time() + (len(line_of_cars['inflate_tires']) * 5)


def diagnostic_time():
    return tire_time() + (len(line_of_cars['diagnostic']) * 30)


def change_oil(request):
    t_no = get_ticket()
    w_time = oil_time()
    line_of_cars['change_oil'].append(t_no)
    ticket = {'no': t_no, 'waiting_time': w_time}

    return render(request, 'ticket.html', {'ticket': ticket})


def inflate_tires(request):
    t_no = get_ticket()
    w_time = tire_time()
    line_of_cars['inflate_tires'].append(t_no)
    ticket = {'no': t_no, 'waiting_time': w_time}

    return render(request, 'ticket.html', {'ticket': ticket})


def diagnostic(request):
    t_no = get_ticket()
    w_time = diagnostic_time()
    line_of_cars['diagnostic'].append(t_no)
    ticket = {'no': t_no, 'waiting_time': w_time}

    return render(request, 'ticket.html', {'ticket': ticket})


def get_queue(request):
    ticket_queue = {
        'change_oil': len(line_of_cars['change_oil']),
        'inflate_tires': len(line_of_cars['inflate_tires']),
        'diagnostic': len(line_of_cars['diagnostic']),
    }
    return render(request, 'processing.html', {'ticket_queue': ticket_queue})


class ProcessNext(View):

    def post(self, request, *args, **kwargs):
        global next_ticket

        if line_of_cars['change_oil']:
            next_ticket = line_of_cars['change_oil'].pop(0)
        elif line_of_cars['inflate_tires']:
            next_ticket = line_of_cars['inflate_tires'].pop(0)
        elif line_of_cars['diagnostic']:
            next_ticket = line_of_cars['diagnostic'].pop(0)
        else:
            next_ticket = -1

        return redirect('/processing/')

    def get(self, request, *args, **kwargs):
        ticket_queue = {
            'change_oil': len(line_of_cars['change_oil']),
            'inflate_tires': len(line_of_cars['inflate_tires']),
            'diagnostic': len(line_of_cars['diagnostic']),
        }
        return render(request, 'processing.html', {'ticket_queue': ticket_queue})


class GetNext(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'next.html', {'next_ticket': next_ticket})
