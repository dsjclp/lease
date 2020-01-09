
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from quote.forms import (
    ScheduleModelForm,
    StepFormset
)
from quote.models import Schedule, Step
from django.http import JsonResponse

def create_quote(request):
    template_name = 'quote/create_quote.html'
    if request.method == 'GET':
        scheduleform = ScheduleModelForm(request.GET or None)
        formset = StepFormset(queryset=Step.objects.none())
    elif request.method == 'POST':
        scheduleform = ScheduleModelForm(request.POST)
        formset = StepFormset(request.POST)
        if scheduleform.is_valid() and formset.is_valid():
            schedule = scheduleform.save(commit=False)
            schedule.user=request.user
            schedule = scheduleform.save()
            i=1
            for form in formset:
                step = form.save(commit=False)
                step.schedule = schedule
                step.rank = i
                step.save()
                i=i+1
            return redirect('dashboard:quote_list')
    return render(request, template_name, {
        'scheduleform': scheduleform,
        'formset': formset,
    })

def quoteAjax(request):
    data = request.POST.get('str')
    import json
    parsed_json = (json.loads(data))
    #print(json.dumps(parsed_json, indent=4, sort_keys=True))
    # create schedule
    saleprice = parsed_json[1]["value"]
    saleprice = int(saleprice)
    rv = parsed_json[2]["value"]
    rv = int(rv)
    # create steps
    step_number = int(parsed_json[3]["value"])
    modelist= []
    numberlist= []
    periodicitylist= []
    amountlist = []
    i=0
    while i < step_number:
        j = int(7 + (4 * i))
        k=i+1
        modelist.insert(k,int(parsed_json[j]["value"]))
        numberlist.insert(k,int(parsed_json[j+1]["value"]))
        periodicitylist.insert(k,int(parsed_json[j+2]["value"]))
        stepamount = parsed_json[j+3]["value"]
        stepamount = int(stepamount) / 100
        stepamount = stepamount * saleprice
        amountlist.insert(k,int(stepamount))
        i=i+1
    #Initialisation de l echeancier mensuel
    echvalue = []
    echcoeff = []
    ind =  0
    #Création des echeanciers mensuels values et coeff
    ind = 0
    indstep = 0
    while indstep < step_number:
        # monthnumber at 1 if periodicity = 0 (monthly)
        if (periodicitylist[indstep] == 0) : periodicitylist[indstep] = 1
        monthnumber = periodicitylist[indstep]
        mois = periodicitylist[indstep]*numberlist[indstep]
        i = 0
        while i < mois:
            k = int(i/monthnumber)
            l = i/monthnumber
            j = ind + i
            m = ind + i + monthnumber
            if (k == l) :
                if (modelist[indstep] == 1) :
                    echvalue.insert(j,amountlist[indstep])
                    echcoeff.insert(j,0)
                if (modelist[indstep] == 0) :
                    echcoeff.insert(j,1)
                    echvalue.insert(j,0)
            if (k != l) :
                echcoeff.insert(j,0)
                echvalue.insert(j,0)
            i=i+1
        ind=mois+ind
        indstep = indstep+1
    #actualisation des values
    rate = 0.05 /12
    i = 0
    npv =  0
    for rent in echvalue:
        val = (float)(echvalue[i] / pow((1+rate),i))
        npv = npv + val
        i=i+1
    npvvalue = npv
    #actualisation des coeffts
    i = 0
    npv =  0
    for rent in echcoeff:
        val = (float)(echcoeff[i] / pow((1+rate),i))
        npv = npv + val
        i=i+1
    npvcoeff = npv
	#calcul de la valeur actuelle de la vr
    npvrv = rv / pow((1+rate),ind)
    #calcul du montant des loyers en coefficient
    npvfin = saleprice - npvvalue - npvrv
    # transmission du résultat
    if (npvcoeff != 0) :
        npvfin = npvfin / npvcoeff
        npvfin = int(npvfin)
    if (npvfin):
        data = str(npvfin)
        echvalue = [10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        crdvalue = [100, 95, 85, 70, 50, 45, 40, 35, 32, 29, 26, 24, 20, 17, 14, 12, 8, 5]
        return JsonResponse(data, safe=False)
    else:
        message="Form is not valid"
        return JsonResponse(message, safe=False)


from django.core import serializers
def detail_quote(request, id):
    template_name = 'quote/detail_quote.html'
    
    #data = serializers.serialize('json', steps)
    echvalue = [10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    crdvalue = [100, 95, 85, 70, 50, 45, 40, 35, 32, 29, 26, 24, 20, 17, 14, 12, 8, 5]

    schedule  = get_object_or_404(Schedule, pk=id)
    schedule.saleprice = 100000
    schedule.vr = 1000
    #Tableau des dettes (CRD)
	#calcul des echeances
    ind=0
    echvalue=[]
    steps = Step.objects.filter(schedule = id)
    for step in steps:
        i = 0
        step.number = 36
        step.amount = 1665
        monthnumber = 1
        mois = step.number * monthnumber
		#balayage des mois internes au module
        while i < mois:
            k = int(i/monthnumber)
            l = i/monthnumber
            j = ind + i
            echvalue.insert(i,0)
            if (l == k):
                echvalue.insert(i,step.amount)
            i=i+1
            ind=mois+ind
			
			#calcul des CRD
            crdvalue = []
            i=0
            crd = schedule.saleprice
            crdfin = schedule.saleprice
            rate = 5 / 120000
            for ech in echvalue:
                crd = crd *(1+rate)
                crdfin = crdfin - echvalue[i]
                crd = crdfin
                crdvalue.insert(i,crd)
                i=i+1

    return render(request, template_name, {'echvalue': echvalue, 'crdvalue': crdvalue})