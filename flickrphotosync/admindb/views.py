import json

from django.contrib import messages
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from admindb.forms import FileUploadForm, AssociationForm


@csrf_exempt
def file_upload(request):
    if request.method == 'POST':
        form = AssociationForm(request.POST)
        if form.is_valid():
            json_data = {'status': 200, 'message': 'success'}
            return HttpResponse(json.dumps(json_data), content_type='application/json')

    file_form = FileUploadForm()

    context = {
        'file_form': file_form,
    }

    return render_to_response('file_upload.html', context_instance=RequestContext(request, context))
