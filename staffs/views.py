from django.shortcuts import render
from fixlyft.models import PickUP as SchedulePickUP
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import UpdateView
# Create your views here.

@staff_member_required
def all_pickups(request):
    pickups = SchedulePickUP.objects.filter(completed=False)
    
    context = {
        'pickups': pickups
    }

    return render(request, 'staffs/pickup.html', context)


class UpdatePickup(UpdateView):
    model = SchedulePickUP
    fields = ['completed',]
    template_name = 'staffs/update.html'