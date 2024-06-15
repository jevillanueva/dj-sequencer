from datetime import datetime
import uuid
from django.http import Http404, HttpResponse
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from .forms import (
    AdminEmissionByDepartmentBatchForm,
    AdminEmissionByDepartmentForm,
    AdminEmissionByDepartmentFormEdit,
    EmissionByDepartmentBatchForm,
    EmissionByDepartmentForm,
    EmissionByDepartmentFormEdit,
    EmissionFileForm,
    EmissionForm,
)
from .models import Department, Emission, EmissionFile, Sequence, UserDepartment


# Create your views here.
@login_required
def index(request):
    user = request.user  # the user
    email = user.email  # their email
    username = user.username  # their username
    # emissions = Emission.objects.filter()
    user_departments = UserDepartment.objects.filter(user=user)
    emissions_by_department = {}
    query = request.GET.get("q")
    # is a date
    query_date = None
    if query:
        try:
            query_date = datetime.strptime(query, "%d/%m/%Y")
        except ValueError:
            query_date = None
    # is a number
    query_number = None
    if query:
        try:
            query_number = int(query)
        except ValueError:
            query_number = None
    for user_department in user_departments:
        department = user_department.department
        if query:
            emissions_list = Emission.objects.filter(
                Q(sequence__department=department)
                & Q(user=user)
                & (
                    Q(detail__icontains=query)
                    | Q(destination__icontains=query)
                    | Q(number=query_number)
                    | Q(date=query_date)
                    | Q(sequence__document__name__icontains=query)
                    | Q(sequence__year__year=query_number)
                )
            ).order_by("received", "-number")
        else:
            emissions_list = Emission.objects.filter(
                user=user, sequence__department=department
            ).order_by("received", "-number")
        paginator = Paginator(emissions_list, 12)
        page_number = request.GET.get(f"page_{department.id}", 1)
        page_obj = paginator.get_page(page_number)
        emissions_by_department[department.id] = page_obj
    tab = request.GET.get(f"tab", 0)
    if not str(tab).isdigit():
        tab = 0
    return render(
        request,
        "emission/index.html",
        {
            "q": query if query else "",
            "emissions_by_department": emissions_by_department,
            "user_departments": user_departments,
            "tab": int(tab),
        },
    )

@login_required
def new(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    department = get_object_or_404(Department, id=uid)
    user_departments = UserDepartment.objects.filter(user=user, department=department)
    if not user_departments:
        raise Http404("No such department")
    sequence = Sequence.objects.filter(department=department, can_emit=True).first()
    if not sequence:
        raise Http404("No sequence available")
    if request.method == "POST":
        form = EmissionByDepartmentForm(
            request.POST, user=request.user, department=department
        )
        if form.is_valid():
            emission = form.save()
            return redirect("emissions:index")
    else:
        form = EmissionByDepartmentForm(user=request.user, department=department)
    return render(request, "emission/emission.html", {"form": form, "emission": None})

@login_required
def new_batch(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    department = get_object_or_404(Department, id=uid)
    user_departments = UserDepartment.objects.filter(user=user, department=department)
    if not user_departments:
        raise Http404("No such department")
    sequence = Sequence.objects.filter(department=department, can_emit=True).first()
    if not sequence:
        raise Http404("No sequence available")
    if request.method == "POST":
        form = EmissionByDepartmentBatchForm(
            request.POST, user=request.user, department=department
        )
        if form.is_valid():
            # Create new batch of emissions
            with transaction.atomic():
                id_batch = uuid.uuid4()
                quantity = int(form.cleaned_data["quantity"])
                current = sequence.sequence
                sequence.increment(quantity)
                emissions = [
                    Emission(
                        sequence=sequence,
                        detail=f'{i}/{quantity}: {form.cleaned_data["detail"]} ({id_batch})',
                        destination=form.cleaned_data["destination"],
                        user=request.user,
                        number=current + i,
                        batch=id_batch,
                    )
                    for i in range(1,quantity+1)
                ]
                Emission.objects.bulk_create(emissions)
                
            return redirect("emissions:index")
    else:
        form = EmissionByDepartmentBatchForm(user=request.user, department=department)
    return render(request, "emission/emission.html", {"form": form, "emission": None})

@login_required
def edit(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    emission = get_object_or_404(Emission, id=uid)
    if emission.user != user:
        raise Http404("No such emission")
    user_departments = UserDepartment.objects.filter(
        user=user, department=emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    if not emission.sequence.can_emit:
        raise Http404("No sequence available")
    if emission.received:
        raise Http404("Emission already received")
    if request.method == "POST":
        form = EmissionByDepartmentFormEdit(
            request.POST,
            user=user,
            department=emission.sequence.department,
            instance=emission,
        )
        if form.is_valid():
            emission = form.save()
            return redirect("emissions:index")
    else:
        form = EmissionByDepartmentFormEdit(
            user=request.user,
            department=emission.sequence.department,
            instance=emission,
        )
    return render(
        request, "emission/emission.html", {"form": form, "emission": emission}
    )


@login_required
def files(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    emission = get_object_or_404(Emission, id=uid)
    if emission.user != user:
        raise Http404("No such emission")
    user_departments = UserDepartment.objects.filter(
        user=user, department=emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    files = EmissionFile.objects.filter(emission=emission)
    return render(
        request, "emission/files.html", {"files": files, "emission": emission}
    )


@login_required
def upload(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    emission = get_object_or_404(Emission, id=uid)
    if emission.user != user:
        raise Http404("No such emission")
    user_departments = UserDepartment.objects.filter(
        user=user, department=emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    if not emission.sequence.can_emit:
        raise Http404("No sequence available")
    if request.method == "POST":
        form = EmissionFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.emission = emission
            # TODO URL if remote file
            # if not file.url:
            #     file.url = file.file.url
            file.save()
            return redirect("emissions:files", id=emission.id)
    else:
        form = EmissionFileForm()
    return render(request, "emission/upload.html", {"form": form, "emission": emission})


@login_required
def delete_file(request, id, idfile):
    user = request.user
    uid = uuid.UUID(id, version=4)
    uidfile = uuid.UUID(idfile, version=4)
    emission = get_object_or_404(Emission, id=uid)
    file = get_object_or_404(EmissionFile, id=uidfile)
    if file.emission.user != user:
        raise Http404("No such emission")
    user_departments = UserDepartment.objects.filter(
        user=user, department=file.emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    if not emission.sequence.can_emit:
        raise Http404("No sequence available")
    file.delete()
    return redirect("emissions:files", id=emission.id)


@login_required
def download_file(request, id, idfile):
    user = request.user
    uid = uuid.UUID(id, version=4)
    uidfile = uuid.UUID(idfile, version=4)
    emission = get_object_or_404(Emission, id=uid)
    file = get_object_or_404(EmissionFile, id=uidfile)
    if file.emission.user != user:
        raise Http404("No such emission")
    user_departments = UserDepartment.objects.filter(
        user=user, department=file.emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    response = HttpResponse(file.file, content_type="application/octet-stream")
    response["Content-Disposition"] = f"attachment; filename={file.file.name}"
    return response


# Create your views here.
@login_required
@permission_required("emission.can_administrate", raise_exception=True)
def admin_index(request):
    user = request.user  # the user
    email = user.email  # their email
    username = user.username  # their username
    # emissions = Emission.objects.filter()
    user_departments = UserDepartment.objects.filter(user=user)
    emissions_by_department = {}
    query = request.GET.get("q")
    # is a date
    query_date = None
    if query:
        try:
            query_date = datetime.strptime(query, "%d/%m/%Y")
        except ValueError:
            query_date = None
    # is a number
    query_number = None
    if query:
        try:
            query_number = int(query)
        except ValueError:
            query_number = None
    for user_department in user_departments:
        department = user_department.department
        if query:
            emissions_list = Emission.objects.filter(
                Q(sequence__department=department)
                & (
                    Q(detail__icontains=query)
                    | Q(destination__icontains=query)
                    | Q(number=query_number)
                    | Q(date=query_date)
                    | Q(sequence__document__name__icontains=query)
                    | Q(sequence__year__year=query_number)
                )
            ).order_by("received", "-number")
        else:
            emissions_list = Emission.objects.filter(
                sequence__department=department
            ).order_by("received", "-number")
        paginator = Paginator(emissions_list, 12)
        page_number = request.GET.get(f"page_{department.id}", 1)
        page_obj = paginator.get_page(page_number)
        emissions_by_department[department.id] = page_obj
    tab = request.GET.get(f"tab", 0)
    if not str(tab).isdigit():
        tab = 0
    return render(
        request,
        "emission/admin_index.html",
        {
            "q": query if query else "",
            "emissions_by_department": emissions_by_department,
            "user_departments": user_departments,
            "tab": int(tab),
        },
    )


@login_required
@permission_required("emission.can_administrate", raise_exception=True)
def admin_new(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    department = get_object_or_404(Department, id=uid)
    user_departments = UserDepartment.objects.filter(user=user, department=department)
    if not user_departments:
        raise Http404("No such department")
    sequence = Sequence.objects.filter(department=department, can_emit=True).first()
    if not sequence:
        raise Http404("No sequence available")
    if request.method == "POST":
        form = AdminEmissionByDepartmentForm(request.POST, department=department)
        if form.is_valid():
            emission = form.save()
            return redirect("emissions:admin_index")
    else:
        form = AdminEmissionByDepartmentForm(department=department)
    return render(request, "emission/emission.html", {"form": form, "emission": None})

@login_required
def admin_new_batch(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    department = get_object_or_404(Department, id=uid)
    user_departments = UserDepartment.objects.filter(user=user, department=department)
    if not user_departments:
        raise Http404("No such department")
    sequence = Sequence.objects.filter(department=department, can_emit=True).first()
    if not sequence:
        raise Http404("No sequence available")
    if request.method == "POST":
        form = AdminEmissionByDepartmentBatchForm(
            request.POST, department=department
        )
        if form.is_valid():
            # Create new batch of emissions
            with transaction.atomic():
                id_batch = uuid.uuid4()
                quantity = int(form.cleaned_data["quantity"])
                current = sequence.sequence
                sequence.increment(quantity)
                emissions = [
                    Emission(
                        sequence=sequence,
                        detail=f'{i}/{quantity}: {form.cleaned_data["detail"]} ({id_batch})',
                        destination=form.cleaned_data["destination"],
                        user=form.cleaned_data["user"],
                        number=current + i,
                        batch=id_batch,
                    )
                    for i in range(1,quantity+1)
                ]
                Emission.objects.bulk_create(emissions)
                
            return redirect("emissions:admin_index")
    else:
        form = AdminEmissionByDepartmentBatchForm(department=department)
    return render(request, "emission/emission.html", {"form": form, "emission": None})

@login_required
@permission_required("emission.can_administrate", raise_exception=True)
def admin_edit(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    emission = get_object_or_404(Emission, id=uid)
    user_departments = UserDepartment.objects.filter(
        user=user, department=emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    if not emission.sequence.can_emit:
        raise Http404("No sequence available")
    if emission.received:
        raise Http404("Emission already received")
    if request.method == "POST":
        form = AdminEmissionByDepartmentFormEdit(
            request.POST,
            department=emission.sequence.department,
            instance=emission,
        )
        if form.is_valid():
            emission = form.save()
            return redirect("emissions:admin_index")
    else:
        form = AdminEmissionByDepartmentFormEdit(
            department=emission.sequence.department,
            instance=emission,
        )
    return render(
        request, "emission/emission.html", {"form": form, "emission": emission}
    )


@login_required
@permission_required("emission.can_administrate", raise_exception=True)
def admin_receive(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    emission = get_object_or_404(Emission, id=uid)
    user_departments = UserDepartment.objects.filter(
        user=user, department=emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    if emission.received:
        raise Http404("Emission already received")
    if request.method == "POST":
        emission.received = True
        emission.user_received = user
        emission.date_received = timezone.now()
        emission.save()
        return redirect("emissions:admin_index")
    else:
        return render(request, "emission/admin_receive.html ", {"emission": emission})


@login_required
@permission_required("emission.can_administrate", raise_exception=True)
def admin_files(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    emission = get_object_or_404(Emission, id=uid)
    user_departments = UserDepartment.objects.filter(
        user=user, department=emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    files = EmissionFile.objects.filter(emission=emission)
    return render(
        request, "emission/admin_files.html", {"files": files, "emission": emission}
    )


@login_required
def admin_upload(request, id):
    user = request.user
    uid = uuid.UUID(id, version=4)
    emission = get_object_or_404(Emission, id=uid)
    user_departments = UserDepartment.objects.filter(
        user=user, department=emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    if request.method == "POST":
        form = EmissionFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.emission = emission
            # TODO URL if remote file
            # if not file.url:
            #     file.url = file.file.url
            file.save()
            return redirect("emissions:admin_files", id=emission.id)
    else:
        form = EmissionFileForm()
    return render(request, "emission/admin_upload.html", {"form": form, "emission": emission})


@login_required
def admin_delete_file(request, id, idfile):
    user = request.user
    uid = uuid.UUID(id, version=4)
    uidfile = uuid.UUID(idfile, version=4)
    emission = get_object_or_404(Emission, id=uid)
    file = get_object_or_404(EmissionFile, id=uidfile)
    user_departments = UserDepartment.objects.filter(
        user=user, department=file.emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    file.delete()
    return redirect("emissions:admin_files", id=emission.id)


@login_required
def admin_download_file(request, id, idfile):
    user = request.user
    uid = uuid.UUID(id, version=4)
    uidfile = uuid.UUID(idfile, version=4)
    emission = get_object_or_404(Emission, id=uid)
    file = get_object_or_404(EmissionFile, id=uidfile)
    user_departments = UserDepartment.objects.filter(
        user=user, department=file.emission.sequence.department
    )
    if not user_departments:
        raise Http404("No such department")
    response = HttpResponse(file.file, content_type="application/octet-stream")
    response["Content-Disposition"] = f"attachment; filename={file.file.name}"
    return response
