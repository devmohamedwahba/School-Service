from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from django.contrib import messages
from django.http import HttpResponse
import datetime
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum

from .models import Student


def main(request):
    return render(request, 'main.html')


@login_required
def home(request):
    queryset = Student.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'topics': topics})


@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            form = StudentForm()

            messages.success(request, 'تم اضافه الطالب بنجاح')
    else:
        form = StudentForm()

    return render(request, 'add_student.html', {'form': form})


@login_required
def student_remove(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    return redirect('home')


def export_csv(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=students' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['المجموع', 'تاريخ الميلاد', 'اسم الطالب']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Student.objects.all().values_list('name', 'birth_date', 'total')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(columns[col_num]), font_style)

    wb.save(response)
    return response


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=students' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    students = Student.objects.all()


    html_string = render_to_string('pdf-html.html', {'students': students, 'total': 0})
    html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')

        response.write(output.read())

    return response
