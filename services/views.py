from django.shortcuts import render


def chip_tuning(request):
    """ a view for the chip tuning page """
    template = 'services/chip_tuning.html'
    context = {
        'title': 'chip tuning',
        'section': 'services',
    }
    return render(request, template, context)


def engine_rebuilds(request):
    """ a view for the engine rebuilds page """
    template = 'services/engine_rebuilds.html'
    context = {
        'title': 'engine rebuilds',
        'section': 'services',
    }
    return render(request, template, context)


def servicing_and_repairs(request):
    """ a view for the servicing and repairs page """
    template = 'services/servicing_and_repairs.html'
    context = {
        'title': 'servicing and repairs',
        'section': 'services',
    }
    return render(request, template, context)


def diagnostics(request):
    """ a view for the diagnostics page """
    template = 'services/diagnostics.html'
    context = {
        'title': 'diagnostics',
        'section': 'services',
    }
    return render(request, template, context)


def custom_exhausts(request):
    """ a view for the custom exhausts page """
    template = 'services/custom_exhausts.html'
    context = {
        'title': 'custom exhausts',
        'section': 'services',
    }
    return render(request, template, context)


def wheel_repair(request):
    """ a view for the wheel repair page """
    template = 'services/wheel_repair.html'
    context = {
        'title': 'wheel repair',
        'section': 'services',
    }
    return render(request, template, context)


def corner_weight_setup(request):
    """ a view for the corner weight setup page """
    template = 'services/corner_weight_setup.html'
    context = {
        'title': 'corner weight setup',
        'section': 'services',
    }
    return render(request, template, context)


def track_drift_preparation(request):
    """ a view for the track drift preparation page """
    template = 'services/track_drift_preparation.html'
    context = {
        'title': 'track/drift preparation',
        'section': 'services',
    }
    return render(request, template, context)
