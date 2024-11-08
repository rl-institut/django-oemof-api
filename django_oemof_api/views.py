# from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.decorators import login_required
import json
import os
import logging
import traceback
import shutil
import zipfile
from django.http import HttpResponseForbidden, JsonResponse
from django.http.response import Http404
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.shortcuts import *
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.views import APIView

# from jsonview.decorators import json_view
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render
from .forms import UploadFileForm
import traceback

logger = logging.getLogger(__name__)


def unzip_scenario_datapackage(zip_file):
    dirname = os.path.join(settings.MEDIA_ROOT, "oemof")
    fullpath = os.path.join(dirname, zip_file)

    package_name = zip_file.replace(".zip", "")
    dirname = os.path.join(settings.MEDIA_ROOT, "oemof", package_name)
    if os.path.exists(dirname):
        logging.warning(f"{dirname} already exists, not overwriting it")
    else:
        os.mkdir(dirname)
        # Unzip the file, creating subdirectories as needed
        zfobj = zipfile.ZipFile(fullpath, mode="r")
        for name in zfobj.namelist():
            if name.endswith("/"):
                try:
                    os.mkdir(os.path.join(dirname, name))
                except FileExistsError:
                    logging.warning(
                        f"{os.path.join(dirname, name)} already exists, not overwriting it"
                    )
            else:
                outfile = open(os.path.join(dirname, name), "wb")
                outfile.write(zfobj.read(name))
                logging.info(f"{os.path.join(dirname, name)} successfully unzipped")
                outfile.close()


class AddDatapackageView(APIView):
    @staticmethod
    def get(request):
        form = UploadFileForm()

        datapackages = default_storage.listdir("oemof")[0]

        return render(
            request,
            "add_datapackage.html",
            {"form": form, "datapackages": datapackages},
        )

    @staticmethod
    def post(request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            zf = form.cleaned_data["file"]
            name = zf.name
            # TODO maybe one can take the fileinmemomry here directly and avoid saving the .zip file
            # store datapakage as zip file
            default_storage.save(f"oemof/{name}", ContentFile(zf.read()))
            zf.close()
            unzip_scenario_datapackage(name)
            # delete the zip file
            default_storage.delete(f"oemof/{name}")
            messages.add_message(
                request, messages.INFO, f"Successfully added {name} scenario"
            )

        return HttpResponseRedirect(reverse("add_datapackage"))


@require_http_methods(["POST"])
def delete_datapackage(request):
    if request.method == "POST":
        scenario_name = request.POST["scenario"]
        scenario_path = os.path.join(settings.MEDIA_ROOT, "oemof", scenario_name)
        if os.path.exists(scenario_path):
            shutil.rmtree(scenario_path)
            messages.add_message(
                request, messages.INFO, f"Successfully deleted '{name}' scenario"
            )
        else:
            messages.add_message(
                request, messages.ERROR, f"Scenario '{name}' does not exist"
            )

        return HttpResponseRedirect(reverse("add_datapackage"))
