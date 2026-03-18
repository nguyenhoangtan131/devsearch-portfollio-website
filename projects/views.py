from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from .utils import searchProjects, paginateProjects

def projects(request):

    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    context = {"projects": projects, "search_query":search_query, 'custom_range': custom_range}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        
        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectObj.id)


    context = {"project": projectObj, "form":form}
    return render(request, "projects/single-project.html", context)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            existing_tag = {t.name.lower(): t for t in Tag.objects.all()}

            for tag in newtags:
                lowertag = tag.lower()
                if lowertag in existing_tag:
                    project.tags.add(existing_tag[lowertag])
                else:
                    tag, created = Tag.objects.get_or_create(name=tag)
                    project.tags.add(tag)
                    existing_tag[lowertag] = tag


            messages.success(request, "Project was added successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(',', " ").split()
        
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            existing_tag = {t.name.lower(): t for t in Tag.objects.all()}

            for tag in newtags:
                lowertag = tag.lower()
                if lowertag in existing_tag:
                    project.tags.add(existing_tag[lowertag])
                else:
                    tag, created = Tag.objects.get_or_create(name=tag)
                    project.tags.add(tag)
                    existing_tag[lowertag] = tag
            
            messages.success(request,"Project was updated successfully!")
            return redirect("account")

    context = {"form": form, "project": project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request,"Projects was deleted successfully!")
        return redirect("account")

    context = {"object": project}
    return render(request, "delete_template.html", context)

